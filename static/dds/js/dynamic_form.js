document.addEventListener('DOMContentLoaded', () => {
    // Очищаем категории и подкатегории при загрузке страницы
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');
    categorySelect.innerHTML = '<option value="">Выберите категорию</option>';
    subcategorySelect.innerHTML = '<option value="">Выберите подкатегорию</option>';

    // Обработка изменения типа
    document.getElementById('id_type').addEventListener('change', async (event) => {
        const typeId = event.target.value;
        categorySelect.innerHTML = '<option value="">Выберите категорию</option>';
        subcategorySelect.innerHTML = '<option value="">Выберите подкатегорию</option>';

        if (typeId) {
            try {
                const response = await fetch(`/get_categories/?type_id=${typeId}`);
                if (!response.ok) throw new Error('Ошибка загрузки категорий');
                const data = await response.json();
                data.categories.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category.id;
                    option.textContent = category.name;
                    categorySelect.appendChild(option);
                });
            } catch (error) {
                alert('Ошибка загрузки категорий. Попробуйте обновить страницу.');
            }
        }
    });

    // Обработка изменения категории
    categorySelect.addEventListener('change', async (event) => {
        const categoryId = event.target.value;
        subcategorySelect.innerHTML = '<option value="">Выберите подкатегорию</option>';

        if (categoryId) {
            try {
                const response = await fetch(`/get_subcategories/?category_id=${categoryId}`);
                if (!response.ok) throw new Error('Ошибка загрузки подкатегорий');
                const data = await response.json();
                data.subcategories.forEach(subcategory => {
                    const option = document.createElement('option');
                    option.value = subcategory.id;
                    option.textContent = subcategory.name;
                    subcategorySelect.appendChild(option);
                });
            } catch (error) {
                alert('Ошибка загрузки подкатегорий. Попробуйте обновить страницу.');
            }
        }
    });
});