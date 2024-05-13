function addToCart(productId) {
    fetch(`/add/${productId}/`);
}


function limparCarrinho() {
    fetch('/clear_cart/')
        .then(response => {
            window.location.href = '/resumo_carrinho/';
        });
}

document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.addToCartBtn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.dataset.productId;
            addToCart(productId);
        });
    });

    const clearCartButton = document.getElementById('clearCartButton');
    const payButton = document.getElementById('payButton');

    if (clearCartButton) {
        clearCartButton.addEventListener('click', limparCarrinho);
    }

});
