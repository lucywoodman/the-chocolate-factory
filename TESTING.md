# The Chocolate Factory Testing

## Table of Contents

- [The Chocolate Factory Testing](#the-chocolate-factory-testing)
  - [Table of Contents](#table-of-contents)
  - [Google's Lighthouse Performance](#googles-lighthouse-performance)
  - [Accessibility Validation](#accessibility-validation)
  - [HTML Validation](#html-validation)
  - [CSS Validation](#css-validation)
  - [JS Validation](#js-validation)
  - [PEP8 Validation](#pep8-validation)
  - [Manual Testing](#manual-testing)
- [Bugs](#bugs)

## Google's Lighthouse Performance

[Google Lighthouse](https://developers.google.com/web/tools/lighthouse) was used to test the performance of the website.

<details><summary>Home page</summary>
<img src="docs/testing/lighthouse-home.png">
</details>

*Go back to the [top](#table-of-contents)*

## Accessibility Validation

The [WAVE WebAIM web accessibility evaluation tool](https://wave.webaim.org/) was used to ensure the website met high accessibility standards. All logged out pages pass with 0 errors.

*Go back to the [top](#table-of-contents)*

## HTML Validation

The [W3C Markup Validation Service](https://validator.w3.org/) was used to validate the HTML of the website. For logged in pages, the page source was copied and pasted into the validator. All pages pass with 0 errors and 0 warnings.

*Go back to the [top](#table-of-contents)*

## CSS Validation

The [W3C Jigsaw CSS Validation Service](https://jigsaw.w3.org/css-validator/validator) was used to validate the CSS of the website. The CSS passes with 0 errors. There are 254 warnings due to Bootstrap's CSS, and 2 warnings for my custom file. The warnings are flaggin up the border and background colours being the same, but this is required to override Bootstrap's styles.

![CSS validation](docs/testing/css.png)

*Go back to the [top](#table-of-contents)*

## JS Validation

[JSHint](https://jshint.com/) was used to validate the JavaScript/Jquery of the website. No issues were found.

![JSHint validation](docs/testing/jshint.png)

*Go back to the [top](#table-of-contents)*

## PEP8 Validation

[PEP8 Online](http://pep8online.com) was used to validate the Python code on the site. The only issues found were a few longer lines in the project's settings.py

![PEP8 valudation](docs/testing/pep8.png)

*Go back to the [top](#table-of-contents)*

## Manual Testing

# Bugs