Class FS.if40recursive Extends %Persistent
{

Property outRole As %String;

Property outEntity As %String;

Property outBaseEntity As %String;

Property outDataBody As %Stream.GlobalBinary;

Property outTemporal As %String;

Property outSpatical As %String;

Property outProperty As %String;

ClassMethod InsertNewpy(R As %String, E As %String, BE As %String, DB As %Binary, T As %String, S As %String, P As %String) As FS.if40recursive [ Language = python ]
{
    import iris

    newdata = iris.cls("FS.if40recursive")._New()
    newdata.outRole = R
    newdata.outEntity = E
    newdata.outBaseEntity = BE
    newdata.outTemporal = T
    newdata.outSpatical = S
    newdata.outProperty = P
    
    newdata.outDataBody.MoveToEnd()

    newdata.outDataBody.Write(DB)
    
    status = newdata._Save()
    id = newdata._Id()
    return id
}

ClassMethod InsertAddpy(DB As %Binary, id As %String) As FS.if40recursive [ Language = python ]
{
    import iris
    #print(len(data))
    add = iris.cls("FS.if40recursive")._OpenId(id)

   
    add.outDataBody.MoveToEnd()

    add.outDataBody.Write(data)
    
    status = add._Save()
    #print(add.ImageData.Size)
    return status
}

ClassMethod ChangeSemantic(numID As %String, R As %String, E As %String, BE As %String, DB As %Binary, T As %String, S As %String, P As %String) As FS.if40recursive [ Language = python ]
{
    import iris

    changedata = iris.cls("FS.if40recursive")._OpenId(numID)
    changedata.outRole = R
    changedata.outEntity = E
    changedata.outBaseEntity = BE
    changedata.outDataBody = DB
    changedata.outTemporal = T
    changedata.outSpatical = S
    changedata.outProperty = P
    status = changedata._Save()
    return status
}

ClassMethod getprogrampy(id As %String, step As %Binary, pos As %Binary) As FS.if40recursive [ Language = python ]
{
    import iris
    result = iris.cls("FS.if40recursive")._OpenId(id)
    #print(result.ImageData.Size)
    result.outDataBody.MoveTo(pos)
    #; while len(bin) < result.outDataBody.Size:
    #;     bin = bin + result.outDataBody.Read(step)
    bin = result.outDataBody.Read(step)
    
    return bin
}

ClassMethod existobject(id As %String) As %Status [ Language = objectscript ]
{
    Set eo = ##class(FS.if40recursive).%ExistsId(id)
    Return eo
}

ClassMethod getmaxID() As FS.if40recursive [ Language = python ]
{
    import iris
    statement = iris.sql.prepare("SELECT MAX(ID) FROM FS.if40recursive")
    rset = statement.execute()
    for row in rset:
        row
    maxID = int(row[0])
    return maxID
}

ClassMethod delobject(id As %String) As %Status [ Language = objectscript ]
{
    Set sc = ##class(FS.if40recursive).%DeleteId(id)
    return sc
}

Storage Default
{
<Data name="if40recursiveDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>outRole</Value>
</Value>
<Value name="3">
<Value>outEntity</Value>
</Value>
<Value name="4">
<Value>outBaseEntity</Value>
</Value>
<Value name="5">
<Value>outDataBody</Value>
</Value>
<Value name="6">
<Value>outTemporal</Value>
</Value>
<Value name="7">
<Value>outSpatical</Value>
</Value>
<Value name="8">
<Value>outProperty</Value>
</Value>
</Data>
<DataLocation>^FS.if40recursiveD</DataLocation>
<DefaultData>if40recursiveDefaultData</DefaultData>
<ExtentSize>40</ExtentSize>
<IdLocation>^FS.if40recursiveD</IdLocation>
<IndexLocation>^FS.if40recursiveI</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,16,$lb("-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000"),$lb(21,21,21,21,21,21,21,21,21,21,21,21,21,21,21),$lb(758198320,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,758198320))</Histogram>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,1,0,$lb(1,3,6,9,12,15,18,21,24,27,30,32,34,36,38,40),$lb(0,0,0,0,1,1,0,1,1,0,1,1,1,1,0),$lb(822083584,822083584,855638016,855638016,905969664,905969664,956301312,956301312,825360384,838860800,889192448,889192448,939524096,825753600,842072064,822083584,872415232,872415232,922746880,842465280,858783744,805306368,838860800,838860800,872415232,872415232,905969664,905969664,939524096,859308032,875560960,875560960))</Histogram>
<Selectivity>1</Selectivity>
</Property>
<Property name="outBaseEntity">
<AverageFieldSize>5</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"),$lb(5,5,5,5,5,5,5,5,5,5,5,5,5,5,5),$lb(541150809,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,541150809))</Histogram>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outDataBody">
<Histogram>$lb(.06666666666666666667,1,0,$lb(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),$lb(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),$lb(805306368,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,805306368))</Histogram>
<Selectivity>2.5000%</Selectivity>
</Property>
<Property name="outEntity">
<AverageFieldSize>5</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" PID"," PID"," PID"," PID"," PID"," PID"," PID"," PID"," PID"," PID"," PID"," PID"," PID"," PID"," PID"," PID"),$lb(5,5,5,5,5,5,5,5,5,5,5,5,5,5,5),$lb(542132548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,542132548))</Histogram>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outProperty">
<AverageFieldSize>46</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"),$lb(50,50,50,50,50,50,50,50,50,50,50,50,50,50,50),$lb(544940614,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,544940614))</Histogram>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outRole">
<AverageFieldSize>5</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" 001"," 003"," 111"," 444"," 777"," AAA"," DDD"," GGG"," JJJ"," MMM"," PPP"," RRR"," TTT"," VVV"," XXX"," ZZZ"),$lb(3,1,1,1,1,1,1,1,1,1,1,1,1,1,1),$lb(540028977,822083584,855638016,808465152,825307392,825307392,875836416,875836416,926365440,926365440,1094795520,1094795520,1145324544,1145324544,1195853568,1195853568,1246382592,1246382592,1296911616,1296911616,1347440640,1347440640,1381126656,1381126656,1414812672,1414812672,1448498688,1448498688,1482184704,1482184704,1515870720,542792282))</Histogram>
<Selectivity>2.5000%</Selectivity>
</Property>
<Property name="outSpatical">
<AverageFieldSize>5</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"),$lb(5,5,5,5,5,5,5,5,5,5,5,5,5,5,5),$lb(541150809,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,541150809))</Histogram>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outTemporal">
<AverageFieldSize>5</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"),$lb(5,5,5,5,5,5,5,5,5,5,5,5,5,5,5),$lb(541150809,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,541150809))</Histogram>
<Selectivity>100.0000%</Selectivity>
</Property>
<SQLMap name="IDKEY">
<BlockCount>-4</BlockCount>
</SQLMap>
<StreamLocation>^FS.if40recursiveS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
