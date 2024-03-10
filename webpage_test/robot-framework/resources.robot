*** Settings ***
Library    RPA.Browser.Selenium

*** Variables ***
${base_url}    https://www.regiojatek.hu/termek-62956-vizipisztoly.html
${product_name}    Vízipisztoly
${product_price}    3995
${cikkszam}    62956
${product_description}    A gyerekek és a felnőttek régen kedvelt, generációkon átívelő játékai közé tartozik a buborékfújó.\nEgy igazi nyári szórakozás már régóta mely még ma is garantálja a jókedvet és a mókát.\nEzek a buborékfújók úgy vannak kialakítva mintha igazi pisztolyok lennének így a gyerkőcök biztosan szeretni fogják ezeket a játékokat.

*** Keywords ***
Open Webpage
    Open Chrome Browser    ${base_url}
Check product name
    ${text}    Get WebElement Text    css:span[property='rdfs:label']
    Should Be Equal    ${text}    ${product_name}    msg=A termék neve nem megfelelő!

Check product price
    ${text}    Get WebElement Text    css:div[class='product-prices product-price']>span
    ${price}    Evaluate    ${text.replace('Ft', '').replace(' ', '')}
    Should Be Equal As Integers  ${price}    ${product_price}    msg=A termék ára nem megfelelő!

Check Product Description
    ${element}    Get WebElement    css: div.prodduct-description
    ${text}    Get Text    ${element}
    Should Be Equal    ${text}    ${product_description}

Add To Cart
    Click Button    css:button[class*="btn-add-to-cart"]

Check Product Name in Cart
    ${text}    Get WebElement Text    css: div.cart-item div span
    ${text}    Evaluate    ${text.replace('Cikkszám: ', '')}
    Should Be Equal As Integers    ${text}    ${cikkszam}

Check Product Item Name In Cart
    ${element}    Get WebElement    css: div.cart-item a > b
    ${name}    Get Text    ${element}
    Should Be Equal    ${name}    ${product_name}


Number Of Products In Cart Should Be 1
    ${element}    Get WebElement    css: input.item_qt
    ${value}    Get Element Attribute    ${element}    value
    Should Be Equal As Integers    ${value}    1


Check Correct Price in Cart
    ${text}    Get WebElement Text    css: div.cart-itemtotal
    ${text}    Evaluate    ${text.replace('Ft', '').replace(' ', '')}
    Should Be Equal As Integers    ${text}        ${product_price} 

Check Subtotal Price
    ${text}    Get WebElement Text    css: div.cart-subtotal > span
    ${text}    Evaluate    ${text.replace('Ft', '').replace(' ', '')}
    Should Be Equal As Integers    ${text}    ${product_price}

Get WebElement Text
    [Arguments]    ${locator}
    ${element}    Get WebElement    ${locator}
    ${text}    Get Text    ${element}
    RETURN    ${text}
