/**
 * Allow increment/decrement of product quantities
 * while preventing out-of-bounds selection by
 * disabling buttons.
 * 
 * Adapted from code by: Code Institute
 *  */

$(document).ready(() => {
    /**
     * Disable +/- buttons outside 1-99 range
     * 
     * @param {int} itemId - product item ID
     */
    const handleEnableDisable = itemId => {
        let currentValue = parseInt($(`#id_qty_${itemId}`).val());
        let minusDisabled = currentValue < 2;
        let plusDisabled = currentValue > 98;
        $(`#decrement-qty_${itemId}`).prop('disabled', minusDisabled);
        $(`#increment-qty_${itemId}`).prop('disabled', plusDisabled);
    }

    // enable/disable all inputs on page load
    let allQtyInputs = $('.qty_input');
    for(let i = 0; i < allQtyInputs.length; i++){
        let itemId = $(allQtyInputs[i]).data('item_id');
        handleEnableDisable(itemId);
    }

    // run enable/disable every time the input is changed
    $('.qty_input').change(function() {
        let itemId = $(this).data('item_id');
        handleEnableDisable(itemId);
    });

    /**
     * Increment quantity of product
     * 
     * @param {event} e - the click event
     */
    $('.increment-qty').click(function(e) {
        e.preventDefault();
        let closestInput = $(this).closest('.input-group').find('.qty_input')[0];
        let currentValue = parseInt($(closestInput).val());
        $(closestInput).val(currentValue + 1);
        let itemId = $(this).data('item_id');
        handleEnableDisable(itemId);
    });

    /**
     * Decrement quantity of product
     *
     * @param {event} e - the click event
     */
    $('.decrement-qty').click(function(e) {
        e.preventDefault();
        let closestInput = $(this).closest('.input-group').find('.qty_input')[0];
        let currentValue = parseInt($(closestInput).val());
        $(closestInput).val(currentValue - 1);
        let itemId = $(this).data('item_id');
        handleEnableDisable(itemId);
    });
});