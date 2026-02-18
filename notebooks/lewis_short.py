import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(about, mo):
    mo.md(f"""
    {about} *About this notebook (including credits info)*
    """)
    return


@app.cell(hide_code=True)
def _(about, mo):
    credits = None
    if about.value:
        credits = mo.md(f"""## About this notebook
    *Version*: **1.0.0**

    ### Motivation

    This addition to the number of programs working with a digital text of Lewis and Short's public-domain *Latin Dictionary* is a marimo notebook written in Python. It can be run locally without an internet connection, or exported as HTML-WASM and dropped in to any web server without any backend requirements or configuration required. These options can sometimes be a convenient alternative to [Christopher Blackwell's app](https://folio3.furman.edu/ls/index.html) that inspired it.

    ### Credits and data sources   

    In the 20th century, the Perseus project digitized the complete text of Lewis and Short in TEI-compliant XML. The full TEI editions can be freely downloaded as part of the [Perseus Greek and Latin texts package](https://www.perseus.tufts.edu/hopper/opensource/download).


    Christopher Blackwell created an edition that extracts essential information from the TEI text and formats articles in Markdown. His markdown lexicon is freely available on github under the terms of a Creative Commons license ([here](https://github.com/Eumaeus/cex_lewis_and_short).

    ### Changelog

    **1.0.0 - 2026-02-18**

    Initial release.

    **Added**

    - search Lewis-Short by headword or article text
    - results sorted by "Blackwell Sort" algorithm
    - view all results at once or in accordion-fold display
        """).callout(kind="info")
    credits    
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Lewis and Short, *Latin Dictionary*
    """)
    return


@app.cell(hide_code=True)
def _(mo, search, search_in, use_accordion):
    mo.md(f"""
    ## Settings


    *Search in* {search_in} 

    *Search for* {search} 

    *Format results as folding blocks* {use_accordion}
    """).callout(kind="info")
    return


@app.cell(hide_code=True)
def _(mo, results_sorted, search):
    hdr = None
    if not search.value:
        hdr = ""
    elif len(results_sorted) == 1:

        hdr = f"## 1 result matching `{search.value}`"

    else:
        hdr = f"## {len(results_sorted)} results matching `{search.value}`"

    mo.md(hdr)    
    return


@app.cell(hide_code=True)
def _(formatdict, formatresults, mo, results_sorted, use_accordion):
    resultsdisplay = None
    if not results_sorted.is_empty():
        if use_accordion.value:
            resultsdisplay = mo.accordion(formatdict(results_sorted))
        else:
            resultsdisplay = mo.md(f"""{formatresults(results_sorted)}""")
    resultsdisplay    
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html("<hr/><hr/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>")
    return


@app.cell(hide_code=True)
def _(mo, show_computation):
    computation = None
    if show_computation:
        computation = mo.md("""
        # Computation
        """)

    computation    
    return


@app.cell
def _(mo):
    meta = mo.app_meta()
    return (meta,)


@app.cell
def _(meta):
    show_computation = meta.mode == 'edit'
    return (show_computation,)


@app.cell(hide_code=True)
def _(mo, show_computation):
    ui = None

    if show_computation:
        ui = mo.md("""
    **UI**
    """)

    ui
    return


@app.cell
def _(mo):
    search = mo.ui.text(debounce=True)
    return (search,)


@app.cell
def _(mo):
    search_in = mo.ui.dropdown(["headword", "article", "all"],value="headword")
    return (search_in,)


@app.cell
def _(mo):
    use_accordion = mo.ui.checkbox()
    return (use_accordion,)


@app.cell
def _(mo):
    about = mo.ui.checkbox()
    return (about,)


@app.cell(hide_code=True)
def _(mo, show_computation):
    disp = None
    if show_computation:    
        disp = mo.md("""
    **Display**
    """)
    disp
    return


@app.cell
def _():
    colnames = {
        "headword": "key",
        "article": "entry"
    }
    return (colnames,)


@app.cell
def _(colnames, search, search_in):
    def formatresults(results):
        if results.is_empty():
            return f"*No matches for* `{search.value}` *in column* `{colnames[search_in.value]}`."

        formatted = []
        for row in results.iter_rows(named=True):
            lemma = row.get("key", "")
            urn = row.get("urn", "")
            text = row.get("entry", "")
            formatted.append(f"## *{lemma}*\n\n`{urn}`\n\n{text}")

        return "\n\n".join(formatted)

    return (formatresults,)


@app.cell
def _(mo, results):
    def formatdict(reslts):
        if results.is_empty():
            return dict()

        articles = {}
        for row in reslts.iter_rows(named=True):
            lemma = row.get("key", "")
            urn = row.get("urn", "")
            text = row.get("entry", "")
            displaystring = f"`{urn}`\n\n{text}"

            articles[lemma] = mo.md(displaystring)

        return articles


    return (formatdict,)


@app.cell(hide_code=True)
def _(mo, show_computation):
    srch = None
    if show_computation:
        srch  = mo.md("""
    **Search**
    """)

    srch
    return


@app.cell
def _(colnames, df, pl, search, search_in):
    if not search.value:
        results = pl.DataFrame()
    else:
        results = df.filter(
            pl.col(colnames[search_in.value]).str.contains(search.value)
        )
    return (results,)


@app.cell
def _(pl, results, search):
    import re

    if not search.value or results.is_empty():
        results_sorted = results
    else:
        escaped_search = re.escape(search.value)
        exact_plus_integer = rf"^{escaped_search}\d+$"

        results_sorted = (
            results.with_columns(
                pl.when(pl.col("key") == search.value)
                .then(pl.lit(1))
                .when(pl.col("key").str.contains(exact_plus_integer))
                .then(pl.lit(2))
                .when(pl.col("key").str.ends_with(search.value))
                .then(pl.lit(3))
                .otherwise(pl.lit(4))
                .alias("group"),
                pl.col("key").str.to_lowercase().alias("_sort_key"),
            )
            .sort(["group", "_sort_key", "key"])
            .drop("_sort_key")
        )
    return (results_sorted,)


@app.cell(hide_code=True)
def _(mo, show_computation):
    datalabel = None
    if show_computation:
        datalabel = mo.md("""
    **Data**
    """)
    datalabel
    return


@app.cell
def _(Path, pl):
    def load_ls():
        datadir = Path.cwd() / "notebooks" / "public"
        lsfile = str(datadir / "ls-articles.cex")
        return pl.read_csv(lsfile, separator="|").with_columns(
            pl.concat_str([pl.col("key"), pl.col("entry")], separator=" ").alias("all")
        )


    return (load_ls,)


@app.cell
def _(load_ls):
    df = load_ls()
    return (df,)


@app.cell(hide_code=True)
def _(mo, show_computation):
    importlabel = None
    if show_computation:
        importlabel = mo.md("""
    **Imports**
    """)

    importlabel
    return


@app.cell
def _():
    from pathlib import Path
    import polars as pl

    return Path, pl


if __name__ == "__main__":
    app.run()
