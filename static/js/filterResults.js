document.addEventListener('DOMContentLoaded', function () {
    const filterSelect = document.getElementById('class-filter');
    filterSelect.addEventListener('change', function () {
        const selectedClass = this.value;
        const resultItems = document.querySelectorAll('.result-item');

        resultItems.forEach(function (item) {
            const itemClasses = item.getAttribute('data-cls').split(',');
            if (selectedClass === 'all' || itemClasses.includes(selectedClass)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });
});
