// Analyst to Architect, Chapter 14, section 14.12 — Power Query (M) cleaning pipeline for orders_q4_2025_export.csv.
// Paste into Excel: Data > Get Data > From Other Sources > Blank Query > Advanced Editor. Change FilePath.
// Needs two helper queries loaded as connections: StatusMap (status_map.csv plus the row cxl) and BranchMap (branch_map.csv, completed to 12 rows); columns raw_value, clean_value; raw_value lower-case.
// Riverstone Supplies is fictional; every name and number is invented.
let
    FilePath   = "C:\Riverstone\ch14\orders_q4_2025_export.csv",
    Source     = Csv.Document(File.Contents(FilePath), [Delimiter = ",", Columns = 13, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted   = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    DataRows   = Table.SelectRows(Promoted, each [order_item_id] <> "" and Text.Select([order_item_id], {"0".."9"}) = [order_item_id]),
    Deduped    = Table.Distinct(DataRows),
    Trimmed    = Table.TransformColumns(Deduped, {{"customer_code", Text.Trim}, {"status", Text.Trim}, {"sales_rep", Text.Trim}, {"branch", Text.Trim}}),
    Keys       = Table.AddColumn(Table.AddColumn(Trimmed, "status_key", each Text.Lower([status])), "branch_key", each Text.Lower([branch])),
    MergedSt   = Table.ExpandTableColumn(Table.NestedJoin(Keys, {"status_key"}, StatusMap, {"raw_value"}, "st", JoinKind.LeftOuter), "st", {"clean_value"}, {"status_clean"}),
    MergedBr   = Table.ExpandTableColumn(Table.NestedJoin(MergedSt, {"branch_key"}, BranchMap, {"raw_value"}, "br", JoinKind.LeftOuter), "br", {"clean_value"}, {"branch_clean"}),
    Code       = Table.AddColumn(MergedBr, "customer_code_clean", each Text.PadStart([customer_code], 4, "0"), type text),
    Parsed     = Table.AddColumn(Code, "order_date_parsed", each
                    let t = Text.Trim([order_date]) in
                    if Text.Length(t) = 5 and Text.Select(t, {"0".."9"}) = t then Date.From(Number.From(t))
                    else try Date.FromText(t, [Format = "dd-MM-yyyy", Culture = "en-IN"])
                    otherwise try Date.FromText(t, [Format = "dd/MM/yyyy", Culture = "en-IN"])
                    otherwise try Date.FromText(t, [Format = "yyyy-MM-dd", Culture = "en-IN"])
                    otherwise null, type nullable date),
    EnteredIST = Table.AddColumn(Parsed, "entered_at_ist", each DateTimeZone.RemoveZone(DateTimeZone.SwitchZone(DateTimeZone.FromText([entered_at_utc]), 5, 30)), type datetime),
    DateFinal  = Table.AddColumn(EnteredIST, "order_date_clean", each if [order_date_parsed] = null then Date.From([entered_at_ist]) else [order_date_parsed], type date),
    Price      = Table.AddColumn(DateFinal, "unit_price_clean", each Number.FromText(Text.Remove(Text.TrimStart([unit_price], {"R", "s", ".", " ", "₹"}), ","), "en-IN"), type number),
    Discount   = Table.AddColumn(Price, "discount_pct_clean", each let d = Number.FromText([discount_pct], "en-IN") in if d > 0 and d < 1 then d * 100 else d, type number),
    Quantity   = Table.AddColumn(Discount, "quantity_clean", each if [quantity] = "" then null else Number.FromText([quantity]) * (if [qty_unit] = "CTN" then 10 else 1), type nullable number),
    Product    = Table.AddColumn(Quantity, "product_id_clean", each if [product_id] <> "" then Number.FromText([product_id])
                    else Record.FieldOrDefault([#"430" = 101, #"750" = 102, #"115" = 103, #"620" = 104, #"1400" = 105, #"1150" = 106, #"380" = 107, #"290" = 108],
                                               Text.From([unit_price_clean]), null), type nullable number),
    Issue      = Table.AddColumn(Product, "issue", each
                    if [quantity_clean] = null then "quantity missing"
                    else if [quantity_clean] > 90 then "quantity above historical maximum"
                    else if [order_date_parsed] = null then "impossible or unreadable date (repaired)"
                    else if [product_id] = "" then "product_id missing (repaired)" else null, type nullable text),
    Final      = Table.SelectColumns(Issue, {"order_item_id", "order_id", "order_date_clean", "customer_code_clean", "product_id_clean", "quantity_clean",
                    "unit_price_clean", "discount_pct_clean", "status_clean", "sales_rep", "branch_clean", "entered_at_ist", "issue"}),
    Typed      = Table.TransformColumnTypes(Final, {{"order_item_id", Int64.Type}, {"order_id", Int64.Type}})
in
    Typed
