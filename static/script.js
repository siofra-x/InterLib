function filterTable() {
    const selectedCurrency = document.getElementById('currency-filter').value; // Get selected currency
    const rows = document.querySelectorAll('table tr[data-currency]'); // Select all rows with the data-currency attribute

    rows.forEach(row => {
        const rowCurrency = row.getAttribute('data-currency'); // Get the currency of the row
        if (selectedCurrency === 'all' || rowCurrency === selectedCurrency) {
            row.style.display = ''; // Show the row
        } else {
            row.style.display = 'none'; // Hide the row
        }
    });
}
 

function addToFavourites(bookId) {
    fetch('/add_to_favourites', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}' // Optional: Add CSRF protection if needed
        },
        body: JSON.stringify({ bookId: bookId })
    })
    .then(response => {
        if (response.ok) {
            alert('Book added to favourites!');
        } else if (response.status === 409) {
            alert('This book is already in your favourites.');
        } else {
            alert('Please log in in order to add to favourites.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to add to favourites.');
    });
}


function makeRowEditable(row) {
    const cells = row.querySelectorAll('.editable');
    const currencySymbol = row.getAttribute('data-currency');

    cells.forEach((cell, index) => {
        const value = cell.textContent.trim();
        
        if (index === 4) {
            // Price: Remove currency symbol and show number input
            const numericValue = value.replace(currencySymbol, '').trim();
            cell.innerHTML = `<input type="number" step="0.01" value="${numericValue}" />`;
        } else if (index === 5) {
            // Purchase URL
            cell.innerHTML = `<input type="text" value="${value}" />`;
        } else {
            // For other fields, just show text input
            cell.innerHTML = `<input type="text" value="${value}" />`;
        }
    });

    const actionCell = row.querySelector('a[href="#"][onclick]');
    actionCell.outerHTML = `
        <button onclick="saveRowChanges(this.closest('tr'))">Save</button>
    `;
}


function saveRowChanges(row) {
const bookId = row.getAttribute('data-book-id');
const currencySymbol = row.getAttribute('data-currency');
const cells = row.querySelectorAll('td');  // Select all <td> elements of the row

// Ensure we have enough cells in the row (index check)
if (cells.length < 6) {
    console.error("Row does not have enough cells to update.");
    return;
}

// Extract data for the fields: Title, Language, Price, and Purchase URL
const updatedData = {
    book_id: bookId,
    title: cells[1].querySelector('input').value.trim(),  // Title is at index 1
    language: cells[2].querySelector('input').value.trim(),  // Language is at index 2
};

// Price: Clean up the value by removing any non-numeric characters (like the currency symbol)
const priceValue = cells[4].querySelector('input').value.trim();  // Get the value from the price input
const numericPrice = parseFloat(priceValue.replace(/[^\d.-]/g, '')); // Remove any non-numeric characters like currency symbol

// Check if the parsed price is valid
if (isNaN(numericPrice)) {
    console.error("Invalid price value:", priceValue);
    alert("Invalid price value.");
    return;  // Exit function if price is invalid
}

updatedData.price = numericPrice;  // Add valid price to the updated data

// Get the purchase URL
updatedData.purchase_url = cells[5].querySelector('input').value.trim();  // Purchase URL is at index 5

// Now update the displayed content of the row
cells[1].textContent = updatedData.title;
cells[2].textContent = updatedData.language;
cells[4].textContent = `${currencySymbol}${updatedData.price.toFixed(2)}`;  // Format price with currency symbol
cells[5].textContent = updatedData.purchase_url;

// Change the "Save" button back to the edit link
const actionCell = row.querySelector('button');
actionCell.outerHTML = `
    <a href="#" onclick="makeRowEditable(this.closest('tr'))" style="color: inherit; text-decoration: none;">
        <i class="fa-solid fa-pen"></i>
    </a>
`;

// Send the updated data to the server
fetch('/edit-book', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'
    },
    body: JSON.stringify(updatedData)
})
.then(response => {
    if (response.ok) {
        alert('Book updated successfully.');
    } else {
        alert('Failed to update the book.');
    }
})
.catch(error => {
    console.error('Error:', error);
    alert('An error occurred while saving the changes.');
});
}

