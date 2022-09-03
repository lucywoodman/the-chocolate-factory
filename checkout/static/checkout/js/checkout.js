/**
* @fileOverview JavaScript for Stripe forms on The Chocolate Factory
*
* Core logic/payment flow comes from:
* https://stripe.com/docs/payments/accept-a-payment
*
* CSS from here:
* https://stripe.com/docs/stripe-js
*/

let stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
let client_secret = $('#id_client_secret').text().slice(1, -1);
const stripe = Stripe(stripe_public_key);

let elements = stripe.elements();
let style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
let card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle realtime errors in Stripe form
card.addEventListener('change', function(e) {
    let errorDiv = document.getElementById('card-errors');
    if (e.error) {
        let html = `<i class="icon fa-solid fa-xmark"></i> ${e.error.message}`;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});