from playwright.sync_api import sync_playwright
import pandas as pd
import io
import re
import time


def clean(x):

    if x:
        return x.strip()

    return ""


def scrape_page(page,url):


    result={

        "URL":url,
        "Title":"",
        "Price":"",
        "Rating":"",
        "Reviews":"",
        "OMSID":"",
        "Badge":""

    }


    page.goto(
        url,
        wait_until="networkidle",
        timeout=60000
    )


    time.sleep(3)


    html=page.content()



    # Title

    try:

        result["Title"]=clean(
            page.locator("h1")
            .first
            .inner_text()
        )

    except:

        pass



    # Price

    try:

        result["Price"]=clean(
            page.locator(
                "[data-testid='product-price']"
            )
            .first
            .inner_text()
        )

    except:

        pass



    # Reviews

    reviews=re.findall(
        r"([\d,]+)\s+Reviews",
        html
    )

    if reviews:

        result["Reviews"]=reviews[0]



    # OMSID

    ids=re.findall(
        r"\d{9}",
        html
    )

    if ids:

        result["OMSID"]=ids[0]



    # Badge

    for badge in [
        "Top Rated",
        "Best Seller"
    ]:

        if badge in html:

            result["Badge"] += badge+" "



    return result, html




def scrape_specs(html,sku):


    specs=[]


    keywords=[
        "Voltage",
        "Warranty",
        "Coverage",
        "Model",
        "Color",
        "Brand",
        "Dimensions"
    ]


    for key in keywords:

        index=html.find(key)


        if index!=-1:

            value=html[index:index+200]


            specs.append({

                "SKU":sku,
                "Specification":key,
                "Value":value

            })


    return specs




def run_scraper(df):


    products=[]

    specifications=[]


    with sync_playwright() as p:


        browser=p.chromium.launch(
            headless=True
        )


        page=browser.new_page()



        for _,row in df.iterrows():


            url=row["URL"]

            sku=row["SKU"]


            product,html=scrape_page(
                page,
                url
            )


            product["SKU"]=sku


            products.append(product)



            specifications.extend(

                scrape_specs(
                    html,
                    sku
                )

            )


        browser.close()



    output=io.BytesIO()



    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:


        pd.DataFrame(products).to_excel(
            writer,
            sheet_name="Product_Info",
            index=False
        )


        pd.DataFrame(specifications).to_excel(
            writer,
            sheet_name="Specifications",
            index=False
        )


    return output.getvalue()
