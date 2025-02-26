(Url as text, Token as text, QuantidadeRegistrosPorPagina as number, OrderBy as text) =>
let
    // Definição do limite máximo de registros por página
    maxRegistrosPorPagina = 500,
    registrosPorPaginaValidos = QuantidadeRegistrosPorPagina <= maxRegistrosPorPagina,

    resultado = if not registrosPorPaginaValidos then
        error "A quantidade máxima de registros por página é 500."
    else
        let
            top = QuantidadeRegistrosPorPagina,

            // Função para buscar registros de uma página específica com tratamento de erro
            request = (skip as number, top as number) =>
            let
                baseURL = Url,
                url = "?$skip=" & Text.From(skip) & "&$top=" & Text.From(top) & "&$orderby=" & Text.From(OrderBy) & "&$filter=year(dueDate) eq 2025",
                response = try Json.Document(Web.Contents("https://api.nibo.com.br",[RelativePath = "empresas/v1/schedules",Query = [#"$skip" = Text.From(skip),#"$top" = Text.From(top),#"$orderby" = Text.From(OrderBy),#"$filter" = "year(dueDate) eq 2025"],Headers = [apitoken = Token]])) otherwise null,
                validResponse = if response <> null and Record.HasFields(response, "items") then response else [items = {}]
            in
                validResponse,

            // Obtendo os dados iniciais da API
            baseURL = Url,
            fonteBruta = try Json.Document(Web.Contents("https://api.nibo.com.br", [RelativePath = "empresas/v1/schedules",Query = [#"$top" = Text.From("1"),#"$filter" = "year(dueDate) eq 2025"],Headers=[apitoken=Token]])) otherwise null,
            Fonte = if fonteBruta <> null and Record.HasFields(fonteBruta, "count") then fonteBruta else [count = 0],

            // Obter o total de registros de forma segura
            totalCount = try Fonte[count] otherwise 0,
            totalPages = Number.RoundUp(Number.From(totalCount) / top),

            // Gerar lista de páginas com tratamento de erro
            listOfPages = List.Generate(
                () => [page = 1, skip = 0, data = request(0, top)], 
                each [page] <= totalPages, 
                each [page = [page] + 1, skip = [skip] + top, data = request([skip] + top, top)]
            ),

            // Criar a tabela inicial
            tabelaInicial = Table.FromList(listOfPages, Splitter.SplitByNothing(), null, null, ExtraValues.Error),

            // Expandir as colunas de forma segura
            tabelaExpandida = Table.ExpandRecordColumn(tabelaInicial, "Column1", {"page", "data"}, {"page", "data"}),

            // Expandir a coluna 'data' apenas se existir 'items'
            tabelaComItems = if Table.HasColumns(tabelaExpandida, "data") then
                Table.ExpandRecordColumn(tabelaExpandida, "data", {"items"}, {"items"})
            else 
                tabelaExpandida,

            #"items Expandido" = if Table.HasColumns(tabelaComItems, "items") then
                Table.ExpandListColumn(tabelaComItems, "items")
            else 
                tabelaComItems,

            // Obter dinamicamente os nomes das colunas e garantir que todos os registros sejam válidos
            colunasItems = if Table.HasColumns(#"items Expandido", "items") then
                List.Distinct(List.Combine(List.Transform(#"items Expandido"[items], each try Record.FieldNames(_) otherwise {})))
            else 
                {},

            // Expandir dinamicamente os campos apenas se existirem registros
            tabelaFinal = if List.Count(colunasItems) > 0 then
                Table.ExpandRecordColumn(#"items Expandido", "items", colunasItems, colunasItems)
            else 
                #"items Expandido"
        in
            tabelaFinal
in
    resultado
