(Url as text, Token as text, QuantidadeRegistrosPorPagina as number, OrderBy as text) =>
let
    // Verificação da quantidade máxima de registros por página
    maxRegistrosPorPagina = 500,
    registrosPorPaginaValidos = QuantidadeRegistrosPorPagina <= maxRegistrosPorPagina,

    // Verificação das condições antes de prosseguir
    resultado = if not registrosPorPaginaValidos then
        error "A quantidade máxima de registros por página é 500."
    else
        let
            // Definição da URL com filtro e ordenação
            url = Url & "?$top=" & Text.From(QuantidadeRegistrosPorPagina) & "&$orderby=" & Text.From(OrderBy) & "&$filter=year(dueDate) eq 2025",
            
            // Obter os dados da API
            Fonte = try Json.Document(Web.Contents(url, [Headers=[apitoken=Token]])) otherwise [],

            // Garante que sempre exista a estrutura esperada
            FonteCorrigida = if Type.Is(Value.Type(Fonte), type record) and Record.HasFields(Fonte, "items")
                then Fonte
                else [items = {}], 

            // Expande a lista de items
            tabelaComItems = Table.FromList(FonteCorrigida[items], Splitter.SplitByNothing(), null, null, ExtraValues.Error),

            // Obter dinamicamente os nomes das colunas dentro de 'items'
            colunasItems = List.Distinct(List.Combine(List.Transform(tabelaComItems[Column1], Record.FieldNames))),

            // Expande dinamicamente os registros dentro de 'items'
            tabelaFinal = Table.ExpandRecordColumn(tabelaComItems, "Column1", colunasItems, colunasItems)
        in
            tabelaFinal
in
    resultado
