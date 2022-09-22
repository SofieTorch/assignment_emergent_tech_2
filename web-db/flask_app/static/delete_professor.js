function delete_professor(professor_id) {
    fetch('/professors', {
        method: 'DELETE',
        body: JSON.stringify({ id: professor_id }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(() => location.reload())
}
