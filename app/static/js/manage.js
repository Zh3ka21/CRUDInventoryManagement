document.addEventListener('DOMContentLoaded', function () {
    // Form submission handlers
    document.getElementById('search-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const searchName = document.getElementById('search_name').value;
        fetch(`/api/products?name=${searchName}`)
            .then(response => response.json())
            .then(data => {
                const productList = document.getElementById('product-list');
                productList.innerHTML = '';
                data.forEach(product => {
                    productList.innerHTML += `
                        <div class="card mb-3">
                            <div class="card-body">
                                <form class="update-form" data-id="${product._id}">
                                    <div class="form-row">
                                        <div class="form-group col-md-2">
                                            <label for="update_name">Name:</label>
                                            <input type="text" class="form-control" name="update_name" value="${product.name}" readonly>
                                        </div>
                                        <div class="form-group col-md-2">
                                            <label for="update_count">Count:</label>
                                            <input type="number" class="form-control" name="update_count" value="${product.count}" required>
                                        </div>
                                        <div class="form-group col-md-4">
                                            <label for="update_description">Description:</label>
                                            <textarea class="form-control" name="update_description">${product.description}</textarea>
                                        </div>
                                        <div class="form-group col-md-2">
                                            <label for="update_category">Category:</label>
                                            <input type="text" class="form-control" name="update_category" value="${product.category}" required>
                                        </div>
                                        <div class="form-group col-md-2">
                                            <label for="update_price_per_unit">Price per Unit ($):</label>
                                            <input type="number" step="0.01" class="form-control" name="update_price_per_unit" value="${product.price_per_unit}" required>
                                        </div>
                                        <div class="form-group col-md-2">
                                            <label for="update_supplier">Supplier:</label>
                                            <input type="text" class="form-control" name="update_supplier" value="${product.supplier}" required>
                                        </div>
                                        <div class="form-group col-md-2 d-flex align-items-end">
                                            <button type="submit" class="btn btn-primary w-100 update-button">Update</button>
                                        </div>
                                        <div class="form-group col-md-2 d-flex align-items-end">
                                            <button type="button" class="btn btn-danger w-100 delete-button">Delete</button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>`;
                });

                // Attach update and delete event listeners
                document.querySelectorAll('.update-form').forEach(form => {
                    form.addEventListener('submit', function (event) {
                        event.preventDefault();
                        const name = form.querySelector('[name="update_name"]').value;
                        const formData = new FormData(this);
                        fetch(`/api/products/${name}`, {
                            method: 'PUT',
                            body: JSON.stringify(Object.fromEntries(formData)),
                            headers: { 'Content-Type': 'application/json' }
                        })
                            .then(response => response.json())
                            .then(data => alert('Product updated successfully!'))
                            .catch(err => alert('Error updating product!'));
                    });
                });

                document.querySelectorAll('.delete-button').forEach(button => {
                    button.addEventListener('click', function () {
                        const name = button.closest('form').querySelector('[name="update_name"]').value;
                        fetch(`/api/products/${name}`, {
                            method: 'DELETE'
                        })
                            .then(response => response.json())
                            .then(data => alert('Product deleted successfully!'))
                            .catch(err => alert('Error deleting product!'));
                    });
                });
            })
            .catch(err => console.error('Error fetching products:', err));
    });

    document.getElementById('add-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/api/products', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(formData)),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => alert('Product added successfully!'))
            .catch(err => alert('Error adding product!'));
    });
});