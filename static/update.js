function updateCompany(el) {
    const company_id = el.value;
    fetch('/current/' + company_id, {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'is_current': el.checked})
    })
    .then(response => {
        if (!response.ok) {
            console.error('Update failed');
        }
    });
}

function addCompany() {
    let companyName = document.getElementById('company_name').value;
    let duration = document.getElementById('work_duration').value;
    
    if (!companyName || !duration) {
        alert('Все поля должны быть заполнены');
        return;
    }

    fetch('/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            'company_name': companyName,
            'work_duration': duration,
            'is_current': true
        })
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        }
    });
}

function clearCompanies() {
    if (confirm("Вы уверены что хотите удалить?")) {
        fetch('/clear', {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'}
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    }
}
