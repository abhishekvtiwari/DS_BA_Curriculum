{# The one definition of net revenue in the whole project (Chapter 13's rule). #}
{% macro net_revenue(quantity, unit_price, discount_pct) -%}
    round({{ quantity }} * {{ unit_price }} * (1 - {{ discount_pct }} / 100.0), 2)
{%- endmacro %}
