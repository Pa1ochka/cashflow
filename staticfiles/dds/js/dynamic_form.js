$(document).ready(function() {
    // очищаем категории и подкатегории при загрузке
    $('#id_category').empty().append('<option value="">Выберите категорию</option>');
    $('#id_subcategory').empty().append('<option value="">Выберите подкатегорию</option>');

    // Обработка изменения типа
    $('#id_type').change(function() {
        var typeId = $(this).val();
        $('#id_category').empty().append('<option value="">Выберите категорию</option>');
        $('#id_subcategory').empty().append('<option value="">Выберите подкатегорию</option>');

        if (typeId) {
            $.ajax({
                url: '/get_categories/',
                data: { 'type_id': typeId },
                success: function(data) {
                    $.each(data.categories, function(index, category) {
                        $('#id_category').append('<option value="' + category.id + '">' + category.name + '</option>');
                    });
                },
                error: function() {
                    alert('Ошибка загрузки категорий. Попробуйте обновить страницу.');
                }
            });
        }
    });

    // Обработка изменения категории
    $('#id_category').change(function() {
        var categoryId = $(this).val();
        $('#id_subcategory').empty().append('<option value="">Выберите подкатегорию</option>');

        if (categoryId) {
            $.ajax({
                url: '/get_subcategories/',
                data: { 'category_id': categoryId },
                success: function(data) {
                    $.each(data.subcategories, function(index, subcategory) {
                        $('#id_subcategory').append('<option value="' + subcategory.id + '">' + subcategory.name + '</option>');
                    });
                },
                error: function() {
                    alert('Ошибка загрузки подкатегорий. Попробуйте обновить страницу.');
                }
            });
        }
    });
});