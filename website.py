from flask import Flask, render_template

app=Flask(__name__)

@app.route("/plot/")
def plot():
    from pandas_datareader import data
    from datetime import datetime
    from bokeh.plotting import show, output_file, figure
    from bokeh.embed import components
    from bokeh.resources import CDN
    import pandas

    def inc_dec(c, o):
        if c > o:
            return "Increase"
        elif c < o:
            return "Decrease"
        else:
            return "Equal"

    start = datetime(2015, 3, 1)
    end = datetime(2016, 3, 10)

    df = data.DataReader(name="AAPL", data_source="iex", start=start, end=end)
    df.index = pandas.to_datetime(df.index)

    df["status"] = [inc_dec(c, o) for c, o in zip(df.close, df.open)]
    df["middle"] = (df.open + df.close) / 2
    df["height"] = abs(df.close - df.open)

    p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")
    p.title.text = "Candlestick"
    p.grid.grid_line_alpha = 0.3

    hours_12 = 12 * 60 * 60 * 1000

    p.segment(df.index, df.high, df.index, df.low, color="Black")

    p.rect(df.index[df.status == "Increase"], df.middle[df.status == "Increase"],
           hours_12, df.height[df.status == "Increase"], fill_color="#CCFFFF", line_color="black")
    p.rect(df.index[df.status == "Decrease"], df.middle[df.status == "Decrease"],
           hours_12, df.height[df.status == "Decrease"], fill_color="#FF3333", line_color="black")

    # output_file("CS.html")
    # show(p)
    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("plot.html", script1=script1,
                           div1=div1,
                           cdn_css=cdn_css,
                           cdn_js=cdn_js)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
