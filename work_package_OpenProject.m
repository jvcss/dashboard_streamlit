let
    Fonte = Json.Document(Web.Contents("https://projects.growthsolutions.com.br/api/v3/projects/42/work_packages?offset=1&pageSize=100&filters=[{ ""status_id"": { ""operator"": ""o"", ""values"": null }}]&sortBy=[[""id"", ""asc""]]")),
    #"Convertido para Tabela" = Record.ToTable(Fonte),
    #"Tabela Transposta" = Table.Transpose(#"Convertido para Tabela"),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(#"Tabela Transposta", [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos",{{"_type", type text}, {"total", Int64.Type}, {"count", Int64.Type}, {"pageSize", Int64.Type}, {"offset", Int64.Type}, {"_embedded", type any}, {"_links", type any}}),
    #"_embedded Expandido" = Table.ExpandRecordColumn(#"Tipo Alterado", "_embedded", {"elements"}, {"_embedded.elements"}),
    #"_embedded.elements Expandido" = Table.ExpandListColumn(#"_embedded Expandido", "_embedded.elements"),
    #"_embedded.elements Expandido1" = Table.ExpandRecordColumn(#"_embedded.elements Expandido", "_embedded.elements", {"derivedStartDate", "derivedDueDate", "spentTime", "laborCosts", "materialCosts", "overallCosts", "_type", "id", "lockVersion", "subject", "description", "scheduleManually", "startDate", "dueDate", "estimatedTime", "derivedEstimatedTime", "remainingTime", "derivedRemainingTime", "duration", "ignoreNonWorkingDays", "percentageDone", "derivedPercentageDone", "createdAt", "updatedAt", "readonly"}, {"_embedded.elements.derivedStartDate", "_embedded.elements.derivedDueDate", "_embedded.elements.spentTime", "_embedded.elements.laborCosts", "_embedded.elements.materialCosts", "_embedded.elements.overallCosts", "_embedded.elements._type", "_embedded.elements.id", "_embedded.elements.lockVersion", "_embedded.elements.subject", "_embedded.elements.description", "_embedded.elements.scheduleManually", "_embedded.elements.startDate", "_embedded.elements.dueDate", "_embedded.elements.estimatedTime", "_embedded.elements.derivedEstimatedTime", "_embedded.elements.remainingTime", "_embedded.elements.derivedRemainingTime", "_embedded.elements.duration", "_embedded.elements.ignoreNonWorkingDays", "_embedded.elements.percentageDone", "_embedded.elements.derivedPercentageDone", "_embedded.elements.createdAt", "_embedded.elements.updatedAt", "_embedded.elements.readonly"}),
    #"Tipo Alterado1" = Table.TransformColumnTypes(#"_embedded.elements Expandido1",{{"_embedded.elements.startDate", type date}, {"_embedded.elements.dueDate", type date}}),
    // Função para converter formato ISO 8601 para horas
    CorrecaoTempoDeTrabalho = (TempoISO as text) as number =>
    let
        // Remove o "P" inicial
        Limpo = Text.Remove(TempoISO, "P"),

        // Separa a parte de dias da parte de tempo (caso exista)
        Partes = Text.Split(Limpo, "T"),
        
        Dias = if List.Count(Partes) > 0 and Text.Contains(Partes{0}, "D") 
            then Number.From(Text.BeforeDelimiter(Partes{0}, "D")) 
            else 0,

        Horas = if List.Count(Partes) > 1 and Text.Contains(Partes{1}, "H") 
                then Number.From(Text.BeforeDelimiter(Partes{1}, "H")) 
                else 0,

        // Converte tudo para horas
        HorasTotais = (Dias * 24) + Horas
    in
        HorasTotais,

    ColunasDuracao = {"_embedded.elements.estimatedTime"},

    TratamentoDuracoes = Table.TransformColumns(
        #"Tipo Alterado1",
        List.Transform(ColunasDuracao, each {_, each if Text.Contains(_, ":") then CorrecaoTempoDeTrabalho(_) else null, type number})
    )
in
    TratamentoDuracoes