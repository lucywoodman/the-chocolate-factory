# The Chocolate Factory Testing

:arrow_left: [Return to the main README](README.md)

## Table of Contents

- [The Chocolate Factory Testing](#the-chocolate-factory-testing)
  - [Table of Contents](#table-of-contents)
  - [Google's Lighthouse Performance](#googles-lighthouse-performance)
  - [Accessibility Validation](#accessibility-validation)
  - [HTML Validation](#html-validation)
  - [CSS Validation](#css-validation)
  - [JS Validation](#js-validation)
  - [PEP8 Validation](#pep8-validation)
  - [Manual Testing (BDD)](#manual-testing-bdd)
  - [Automated Testing (TDD)](#automated-testing-tdd)
- [Bugs](#bugs)

## Google's Lighthouse Performance

[Google Lighthouse](https://developers.google.com/web/tools/lighthouse) was used to test the performance of the website.

<details><summary>Home page</summary>
<img src="docs/testing/lighthouse-home.png">
</details>

*Go back to the [top](#table-of-contents)*

---

## Accessibility Validation

The [WAVE WebAIM web accessibility evaluation tool](https://wave.webaim.org/) was used to ensure the website met high accessibility standards. All pages pass with 0 errors, except for the Profile page and Checkout page. This is due to the forms not using labels. With more time I can dig into this, however, for now it has been saved as an open issue on the Github repository.

*Go back to the [top](#table-of-contents)*

---

## HTML Validation

The [W3C Markup Validation Service](https://validator.w3.org/) was used to validate the HTML of the website. For logged in pages, the page source was copied and pasted into the validator. All pages pass with 0 errors and 0 warnings.

*Go back to the [top](#table-of-contents)*

---

## CSS Validation

The [W3C Jigsaw CSS Validation Service](https://jigsaw.w3.org/css-validator/validator) was used to validate the CSS of the website. The CSS passes with 0 errors.

![CSS validation](docs/testing/css.png)

*Go back to the [top](#table-of-contents)*

---

## JS Validation

[JSHint](https://jshint.com/) was used to validate the JavaScript/Jquery of the website. No issues were found.

![JSHint validation](docs/testing/jshint.png)

*Go back to the [top](#table-of-contents)*

---

## PEP8 Validation

A combination of the following Python packages was used to ensure the code is PEP8 compliant: flake8, autopep8 and black. After which `flake8 --statistics` was ran in VSCode terminal and the final flagged files were checked in [PEP8 Online](http://pep8online.com). The only issues found were a few longer lines in the project's settings.py.

![PEP8 valudation](docs/testing/pep8.png)

*Go back to the [top](#table-of-contents)*

---

## Manual Testing (BDD)

BDD, or Behaviour Driven Development, is the process used to test user stories in a non-technical way, allowing anyone to test the features of an app.

Given some context, When something happens, Then outcome

User Story | BDD Test | Pass
--- | --- | :---:
As a user<br>I want to see an interesting homepage<br>So that I can learn about the store and the type of products it sells | Given that I'm a new visitor to the website<br>When I view/scroll down the homepage<br>Then I should see what they sell and what they care about | :white_check_mark:
As a user<br>I want to subscribe to a newsletter<br>So that I can receive updates about the store | Given that I am not already subscribed<br>When I click the "Click to subscribe" button in the footer and enter my email address<br>Then I should see confirmation that I have subscribed to the newsletter | :white_check_mark:
As a user<br>I want to register my profile<br>So that I can save my personal information for future shopping | Given that I'm not already registered<br>When I click on "Account" -> "Register" and submit my information<br>Then I should see confirmation that my profile has been created and I should be able to login | :white_check_mark:
As a user<br>I want to view the list of products available<br>So that I can see what the store has to offer | Given that I'm on the homepage<br>When I click on the "Explore Store" button or "Full Range" -> "All Products"<br>Then I should be taken to the Products page where I can see all of the products available | :white_check_mark:
As a user<br>I want to see the products filtered by category<br>So that I can narrow down the products and find what I need easier | Given that I'm on the homepage<br>When I click on "Full Range" and a category<br>Then I should only see that particular category's products | :white_check_mark:
As a user<br>I want to filter the products<br>So that I can narrow down my search | Given that I'm on the Products page<br>When I click on "Filter by" and choose an option<br>Then I expect to only see the products related to that specific filter | :white_check_mark:
As a user<br>I want to search for specific products<br>So that I can avoid clicking through pages | Given that I want to search for "white chocolate"<br>When I type this into the search form and click search<br>Then I should only see products that mention "white chocolate" in their title or description | :white_check_mark:
As a user<br>I want to add products to my bag<br>So that I can save what I might purchase | Given that I'm on a Product Detail page<br>When I click on "Add to bag"<br>Then I should see confirmation that my item has been added to the bag and be able to see it in the mini-bag/Bag | :white_check_mark:
As a user<br>I want to remove products from my bag<br>So that I can edit the order before checking out | Given that my bag is not empty and I'm on the Bag page<br>When I click on the trash icon<br>Then I expect the item to be removed from the bag and to see confirmation of this | :white_check_mark:
As a user<br>I want to edit the quantities of items in my bag<br>So that I can edit the order before checking out | Given that my bag is not empty and I'm on the Bag page<br>When I click on the plus or minus buttons, followed by "Update order"<br>Then I should see the quantity and order totals update | :white_check_mark:
As a user<br>I want to go through a checkout process<br>So that I can review my bag and add my details to complete my purchase | Given that I'm on the mini-bag/Bag page<br>When I click on "Secure Checkout"<br>Then I should see a form where I can enter my details to start the checkout process | :white_check_mark:
As a user<br>I want to provide card details<br>So that I can pay for the products in my cart | Given that I'm on the Secure Checkout page<br>When I've filled in my details and scrolled down<br>Then I should see a section where I can enter my payment details | :white_check_mark:
As a user<br>I want to have my payment processed<br>So that I can complete my order | Given that I've entered my personal details and card details on the Secure Checkout page<br>When I click the "Pay Now" button<br>Then I should see confirmation that all is well and my order has been received | :white_check_mark:
As a user that's logged in<br>I want my details to be autofilled at checkout<br>So that I can make purchase quicker and easier | Given that I've already filled in my profile information<br>When I next go to checkout<br>Then I should see my details already populated in the checkout form | :white_check_mark:
As a user<br>I want to see feedback on my actions<br>So that I can get confirmation of the actions I've taken | Given that I'm taking action on the site<br>When I complete the action<br>I should see a notifcation letting me know what I've done/not done | :white_check_mark:
As a superuser<br>I want to add products to the store<br>So that I can offer products to seel and add new products in the future | Given that I'm a logged in superuser<br>When I click on "Account" -> "Product Management"<br>Then I should be able to complete the form and submit for new products to be added to the store | :white_check_mark:
As a superuser<br>I want to update products<br>So that I can keep them up to date | Given that I'm a logged in superuser and on the Products or Product Detail page<br>When I click on "Update product"<br>Then I should see a form to be able to edit that specific product | :white_check_mark:
As a superuser<br>I want to delete products<br>So that users won't buy unavailable products | Given that I'm a logged in superuser and on the Products or Product Detail page<br>When I click on the "Delete product" button<br>Then I should see a modal asking me for confirmation before I delete the product, then delete the product once I confirm | :white_check_mark:
As a superuser<br>I want to send newsletters to our mailing list<br>So that I can share store news | Given that I'm logged into the Mailchimp account<br>When I view the contact list<br>Then I should see a list of subscribers who I can then set up an email campaign for | :white_check_mark:

*Go back to the [top](#table-of-contents)*

---

## Automated Testing (TDD)

TDD, or Test Driven Development, was used throughout parts of the development process. Using Django's testing class, I created 44 tests which all pass. Using `coverage`, testing covers 72% of the code. Ideally, this would be above 90% with more time devoted to it.

![Automated testing](docs/testing/automated.png)

*Go back to the [top](#table-of-contents)*

---

# Bugs

*Go back to the [top](#table-of-contents)*

---