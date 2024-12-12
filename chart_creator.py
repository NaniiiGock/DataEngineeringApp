import altair as alt
import plotly.express as px

class ChartCreator:
    def __init__(self):
        pass

    def create_chart1(self, df) -> alt.Chart:
        line_chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('month', title="Month"),
            y=alt.Y('sales', title="Sales (USD)", scale=alt.Scale(domain=[0, df['sales'].max() + 2000])),
            tooltip=['month', 'sales']
        ).properties(
            width=700,
            height=400,
            title="Sales Trend Over the Year"
        ).configure_title(
            fontSize=20,
            font="Arial",
            anchor="middle"
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )
        return line_chart
    
    def create_chart2(self, df):
        bar_chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10).encode(
                x=alt.X('product_category', title="Product Category", sort='-y'),
                y=alt.Y('sales', title="Sales (USD)"),
                color=alt.Color('product_category', legend=None),
                tooltip=['product_category', 'sales']
            ).properties(
                width=700,
                height=400,
                title="Product Category Sales"
            ).configure_title(
                fontSize=20,
                font="Arial",
                anchor="middle"
            ).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            )
        return bar_chart

    def create_chart3(self, df):
        scatter_chart = px.scatter(
            df,
            x="investment",
            y="roi",
            labels={"investment": "Investment (USD)", "roi": "Return on Investment (USD)"},
            title="Ad Campaign Performance",
            color="investment",
            size="roi",
            hover_data={"investment": True, "roi": True},
            template="plotly_dark",
        )
        scatter_chart.update_traces(marker=dict(size=12, line=dict(width=1, color="DarkSlateGrey")))
        scatter_chart.update_layout(
            title_font_size=20,
            font=dict(size=14),
            height=500,
            width=800,
        )
        return scatter_chart
    
    
