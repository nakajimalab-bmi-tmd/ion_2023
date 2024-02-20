Class FS.if50 Extends %Persistent
{

Property outRole As %String;

Property outEntity As %String;

Property outBaseEntity As %String;

Property outDataBody As %Stream.GlobalBinary;

Property outTemporal As %String;

Property outSpatical As %String;

Property outProperty As %String;

ClassMethod InsertNewpy(R As %String, E As %String, BE As %String, DB As %Binary, T As %String, S As %String, P As %String) As FS.if50 [ Language = python ]
{
    import iris

    newdata = iris.cls("FS.if50")._New()
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

ClassMethod InsertAddpy(DB As %Binary, id As %String) As FS.if50 [ Language = python ]
{
    import iris
    #print(len(data))
    add = iris.cls("FS.if50")._OpenId(id)

   
    add.outDataBody.MoveToEnd()

    add.outDataBody.Write(data)
    
    status = add._Save()
    #print(add.ImageData.Size)
    return status
}

ClassMethod ChangeSemantic(numID As %String, R As %String, E As %String, BE As %String, DB As %Binary, T As %String, S As %String, P As %String) As FS.if50 [ Language = python ]
{
    import iris

    changedata = iris.cls("FS.if50")._OpenId(numID)
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

ClassMethod getprogrampy(id As %String, step As %Binary, pos As %Binary) As FS.if50 [ Language = python ]
{
    import iris
    result = iris.cls("FS.if50")._OpenId(id)
    #print(result.ImageData.Size)
    result.outDataBody.MoveTo(pos)
    #; while len(bin) < result.outDataBody.Size:
    #;     bin = bin + result.outDataBody.Read(step)
    bin = result.outDataBody.Read(step)
    
    return bin
}

ClassMethod existobject(id As %String) As %Status [ Language = objectscript ]
{
    Set eo = ##class(FS.if50).%ExistsId(id)
    Return eo
}

ClassMethod getmaxID() As FS.if50 [ Language = python ]
{
    import iris
    statement = iris.sql.prepare("SELECT MAX(ID) FROM FS.if50")
    rset = statement.execute()
    for row in rset:
        row
    maxID = int(row[0])
    return maxID
}

ClassMethod delobject(id As %String) As %Status [ Language = objectscript ]
{
    Set sc = ##class(FS.if50).%DeleteId(id)
    return sc
}

Storage Default
{
<Data name="if50DefaultData">
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
<DataLocation>^FS.if50D</DataLocation>
<DefaultData>if50DefaultData</DefaultData>
<ExtentSize>50</ExtentSize>
<IdLocation>^FS.if50D</IdLocation>
<IndexLocation>^FS.if50I</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,16,$lb("-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000"),$lb(21,21,21,21,21,21,21,21,21,21,21,21,21,21,21),$lb(758198320,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,758198320))</Histogram>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,1,0,$lb(1,4,8,12,16,20,23,26,29,32,35,38,41,44,47,50),$lb(0,0,0,1,0,1,1,1,0,1,1,0,1,1,0),$lb(822083584,822083584,872415232,872415232,939524096,939524096,825360384,838860800,905969664,825622528,842006528,805306368,855638016,855638016,905969664,905969664,956301312,842596352,858914816,838860800,889192448,889192448,939524096,859308032,875626496,822083584,872415232,872415232,922746880,876019712,892338176,892338176))</Histogram>
<Selectivity>1</Selectivity>
</Property>
<Property name="outBaseEntity">
<AverageFieldSize>5</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"," ANY"),$lb(5,5,5,5,5,5,5,5,5,5,5,5,5,5,5),$lb(541150809,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,541150809))</Histogram>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outDataBody">
<Histogram>$lb(.06666666666666666667,1,0,$lb(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),$lb(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),$lb(805306368,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,805306368))</Histogram>
<Selectivity>2.0000%</Selectivity>
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
<Histogram>$lb(.06666666666666666667,0,0,$lb(" 001"," 004"," 008"," 012"," 111"," 555"," 888"," BBB"," EEE"," HHH"," KKK"," NNN"," QQQ"," TTT"," WWW"," ZZZ"),$lb(3,3,2,1,1,1,1,1,1,1,1,1,1,1,1),$lb(540028977,822083584,872415232,872415232,939524096,808976384,825360384,808530432,825307392,825307392,892679424,892679424,943208448,943208448,1111638528,1111638528,1162167552,1162167552,1212696576,1212696576,1263225600,1263225600,1313754624,1313754624,1364283648,1364283648,1414812672,1414812672,1465341696,1465341696,1515870720,542792282))</Histogram>
<Selectivity>2.0000%</Selectivity>
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
<StreamLocation>^FS.if50S</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
