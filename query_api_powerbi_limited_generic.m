(ProjetoId as number, Token as text, Offset as number, PageSize as number, Filters as text, SortBy as text) =>
let
    // Definição do domínio fixo e caminho base da API
    Dominio = "https://projects.growthsolutions.com.br",
    CaminhoBase = "/api/v3/projects/" & Text.From(ProjetoId) & "/work_packages",

    // Parâmetros de consulta organizados no formato correto
    QueryParams = [
        offset = Text.From(Offset),
        pageSize = Text.From(PageSize),
        filters = Filters,
        sortBy = SortBy
    ],

    // Configuração dos cabeçalhos HTTP
    Headers = [
        Authorization = "Basic " & Token
    ],

    // Chamada à API usando Web.Contents com RelativePath e Query
    Fonte = try Json.Document(Web.Contents(Dominio, [
        RelativePath = CaminhoBase,
        Query = QueryParams,
        Headers = Headers
    ])) otherwise null,

    // Garante que sempre exista a estrutura esperada
    FonteCorrigida = if Type.Is(Value.Type(Fonte), type record) and Record.HasFields(Fonte, "_embedded") 
        then Fonte
        else [_embedded = [work_packages = {}]],

    // Obtém os dados da resposta e converte em tabela
    TabelaItems = try Table.FromList(FonteCorrigida[_embedded][work_packages], Splitter.SplitByNothing(), null, null, ExtraValues.Error) otherwise #table({}, {}),

    // Extrai dinamicamente os nomes das colunas (se houver dados)
    Colunas = if Table.RowCount(TabelaItems) > 0 then
                List.Distinct(List.Combine(List.Transform(TabelaItems[Column1], Record.FieldNames)))
              else {},

    // Expande dinamicamente os registros dentro de 'items'
    TabelaFinal = if List.Count(Colunas) > 0 then
                    Table.ExpandRecordColumn(TabelaItems, "Column1", Colunas, Colunas)
                  else
                    TabelaItems
in
    TabelaFinal
