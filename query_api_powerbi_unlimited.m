= (Url as text, Token as text, QuantidadeRegistrosPorPagina as number, OrderBy as text) =>
let
    
    // Verificação da quantidade máxima de registros por página
    maxRegistrosPorPagina = 500,
    registrosPorPaginaValidos = QuantidadeRegistrosPorPagina <= maxRegistrosPorPagina,

    // Verificação das condições antes de prosseguir
    resultado = if not registrosPorPaginaValidos then
        error "A quantidade máxima de registros por página é 500."
    else
        let
            // Visualização de registros
            top = QuantidadeRegistrosPorPagina,

            // Função para buscar os registros de uma página específica
            request = (skip as number, top as number) =>
            let
                baseURL = Url,
                url = baseURL & "?$skip=" & Text.From(skip) & "&$top=" & Text.From(top) & "&$orderby=" & Text.From(OrderBy),
                Fonte = Json.Document(Web.Contents(url, [Headers=[apitoken=Token]]))
            in
                Fonte,

            // Definindo a URL base
            baseURL = Url,
            Fonte = Json.Document(Web.Contents(baseURL, [Headers=[apitoken=Token]])),
            totalCount = Fonte[count], // Total de registros
            totalPages = Number.RoundUp(totalCount / top),

            // Gerar lista de páginas, incluindo o número da página em cada registro
            listOfPages = List.Generate(
                () => [page = 1, skip = 0, data = request(0, top)], // Estado inicial
                each [page] <= totalPages, // Condição de repetição
                each [page = [page] + 1, skip = [skip] + top, data = request([skip] + top, top)]
            ),

            // Converter para tabela
            tabelaInicial = Table.FromList(listOfPages, Splitter.SplitByNothing(), null, null, ExtraValues.Error),

            // Expandir os campos 'page' e 'data'
            tabelaExpandida = Table.ExpandRecordColumn(tabelaInicial, "Column1", {"page", "data"}, {"page", "data"}),

            // Expandir a coluna 'data' para obter 'items'
            tabelaComItems = Table.ExpandRecordColumn(tabelaExpandida, "data", {"items"}, {"items"}),
            
            #"items Expandido" = Table.ExpandListColumn(tabelaComItems, "items"),
    
            // Obter dinamicamente os nomes das colunas dos registros dentro de 'items'
            colunasItems = List.Distinct(List.Combine(List.Transform(#"items Expandido"[items], Record.FieldNames))),
    
            // Expandir dinamicamente os campos de cada registro dentro de 'items'
            tabelaFinal = Table.ExpandRecordColumn(#"items Expandido", "items", colunasItems, colunasItems)
        in
            tabelaFinal
in
    resultado