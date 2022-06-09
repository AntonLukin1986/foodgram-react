def download_pdf(to_buy, HttpResponse, pdfmetrics,
                 TTFont, Canvas, Recipe, request):
    """Скачивание файла в формате pdf."""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.pdf"'
    )
    pdfmetrics.registerFont(
        TTFont(
            'Amstelvar_Roman',
            'D:/dev/foodgram-project-react/data/Amstelvar_Roman.ttf', 'UTF-8')
        )
    page = Canvas(response)
    # настройки для заголовка
    page.setFont('Amstelvar_Roman', size=20)
    page.drawString(200, 780, 'СПИСОК ИНГРЕДИЕНТОВ')  # отступы слева, снизу
    # настройки для основного текста
    page.setFont('Amstelvar_Roman', size=18)
    margin = 740
    for i, (name, data) in enumerate(to_buy.items(), 1):
        page.drawString(72, margin, (f'{i}.  {name}  -  {data[0]} '
                                     f'{data[1]}'))
        margin -= 30
    recipes = {'name': item.name for item in Recipe.objects.filter(
        user_carts__user=request.user
    ).order_by('name')}
    page.drawString(72, margin - 30, 'для приготовления:')
    margin -= 60
    for recipe_name in recipes.values():
        page.drawString(72, margin, recipe_name)
        margin -= 30
    page.save()
    return response


def download_txt(to_buy, Recipe, request, HttpResponse, status):
    """Скачивание файла в формате txt."""
    result_list = '\tСписок продуктов:\n\n'
    for i, (name, quantity_unit) in enumerate(to_buy.items(), 1):
        result_list += (
            str(i) + '. ' + name + ':  ' +
            str(quantity_unit[0]) + ' ' + quantity_unit[1] + '\n'
        )
    result_list += '\nдля приготовления:\n'
    for recipe in Recipe.objects.filter(
        user_carts__user=request.user
    ).order_by('name'):
        result_list += '~' + recipe.name + '\n'
    response = HttpResponse(
        result_list, content_type='plain/txt', status=status.HTTP_200_OK
    )
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.txt"'
    )
    return response
