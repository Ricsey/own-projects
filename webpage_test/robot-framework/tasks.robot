*** Settings ***
Documentation       Product page verification and check "Add to cart" functionality.
Resource    resources.robot

Suite Setup    Open Webpage
Suite Teardown    Close All Browsers

*** Tasks ***
Check product webpage
    Check product name
    Check product price
    Check Product Description

Check adding to cart
    Add To Cart
    Check Product Name in Cart
    Check Product Item Name In Cart
    Number Of Products In Cart Should Be 1
    Check Correct Price in Cart
    Check Subtotal Price    
    