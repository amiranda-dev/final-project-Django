function autoComplete(inputSelector) {
    var inputElement = $(inputSelector);
    var buscaUrl = inputElement.data('url');
    var hiddenSelector = inputElement.data('hidden');

    $(inputSelector).autocomplete({
        minLength: 3, // SÓ PESQUISA APÓS 3 LETRAS
        delay: 500,   // ESPERA 0,5 SEGUNDOS APÓS O ÚLTIMO CLIQUE
        source: function(request, response) {
            $.ajax({
                url: buscaUrl,
                dataType: "json",
                data: { q: request.term },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item.nome,
                            value: item.nome,
                            id: item.id
                        };
                    }));
                }
            });
        },
        select: function(event, ui) {
            $(hiddenSelector).val(ui.item.id);
        }
    });
}