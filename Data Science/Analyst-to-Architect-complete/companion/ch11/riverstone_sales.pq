// Analyst to Architect, Chapter 11, section 11.7 — Power Query (M) for Riverstone's monthly exports.
// Paste into Excel: Data > Get Data > From Other Sources > Blank Query > Advanced Editor. Change FolderPath.
// Riverstone Supplies is fictional; every name and number is invented.
let
    FolderPath = "C:\Riverstone\monthly_exports",
    Source     = Folder.Files(FolderPath),
    CsvOnly    = Table.SelectRows(Source,
                     each Text.Lower([Extension]) = ".csv"),
    Parsed     = Table.AddColumn(CsvOnly, "Data",
                     each Table.PromoteHeaders(
                         Csv.Document([Content],
                             [Delimiter = ",", Encoding = 65001,
                              QuoteStyle = QuoteStyle.Csv]),
                         [PromoteAllScalars = true])),
    Combined   = Table.Combine(Parsed[Data]),
    Typed      = Table.TransformColumnTypes(Combined, {
                     {"order_id", Int64.Type},
                     {"customer_code", type text},
                     {"product_id", Int64.Type},
                     {"quantity", Int64.Type},
                     {"unit_price", type number},
                     {"discount_pct", type number},
                     {"status", type text},
                     {"sales_rep", type text}}),
    TypedDates = Table.TransformColumnTypes(Typed,
                     {{"order_date", type date}}, "en-IN"),
    Valid      = Table.SelectRows(TypedDates,
                     each [status] <> "Cancelled"),
    NetRevenue = Table.AddColumn(Valid, "net_revenue",
                     each [quantity] * [unit_price]
                          * (1 - [discount_pct] / 100),
                     type number)
in
    NetRevenue
