Class FS.if30re Extends %Persistent
{

Property outRole As %String;

Property outEntity As %String;

Property outBaseEntity As %String;

Property outDataBody As %Stream.GlobalBinary;

Property outTemporal As %String;

Property outSpatical As %String;

Property outProperty As %String;

ClassMethod InsertNewpy(R As %String, E As %String, BE As %String, DB As %Binary, T As %String, S As %String, P As %String) As FS.if30re [ Language = python ]
{
    import iris

    newdata = iris.cls("FS.if30re")._New()
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

ClassMethod InsertAddpy(DB As %Binary, id As %String) As FS.if30re [ Language = python ]
{
    import iris
    #print(len(data))
    add = iris.cls("FS.if30re")._OpenId(id)

   
    add.outDataBody.MoveToEnd()

    add.outDataBody.Write(data)
    
    status = add._Save()
    #print(add.ImageData.Size)
    return status
}

ClassMethod ChangeSemantic(numID As %String, R As %String, E As %String, BE As %String, DB As %Binary, T As %String, S As %String, P As %String) As FS.if30re [ Language = python ]
{
    import iris

    changedata = iris.cls("FS.if30re")._OpenId(numID)
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

ClassMethod getprogrampy(id As %String, step As %Binary, pos As %Binary) As FS.if30re [ Language = python ]
{
    import iris
    result = iris.cls("FS.if30re")._OpenId(id)
    #print(result.ImageData.Size)
    result.outDataBody.MoveTo(pos)
    #; while len(bin) < result.outDataBody.Size:
    #;     bin = bin + result.outDataBody.Read(step)
    bin = result.outDataBody.Read(step)
    
    return bin
}

ClassMethod existobject(id As %String) As %Status [ Language = objectscript ]
{
    Set eo = ##class(FS.if30re).%ExistsId(id)
    Return eo
}

ClassMethod getmaxID() As FS.if30re [ Language = python ]
{
    import iris
    statement = iris.sql.prepare("SELECT MAX(ID) FROM FS.if30re")
    rset = statement.execute()
    for row in rset:
        row
    maxID = int(row[0])
    return maxID
}

ClassMethod delobject(id As %String) As %Status [ Language = objectscript ]
{
    Set sc = ##class(FS.if30re).%DeleteId(id)
    return sc
}

Storage Default
{
<Data name="if30reDefaultData">
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
<DataLocation>^FS.if30reD</DataLocation>
<DefaultData>if30reDefaultData</DefaultData>
<ExtentSize>30</ExtentSize>
<IdLocation>^FS.if30reD</IdLocation>
<IndexLocation>^FS.if30reI</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,16,$lb("-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000","-10000000000000000000"),$lb(21,21,21,21,21,21,21,21,21,21,21,21,21,21,21),$lb(758198320,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,758198320))</Histogram>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,1,0,$lb(1,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30),$lb(0,0,0,0,0,1,1,1,1,0,1,1,1,1,0),$lb(822083584,822083584,838860800,838860800,872415232,872415232,905969664,905969664,939524096,939524096,825229312,805306368,838860800,838860800,872415232,872415232,905969664,905969664,939524096,825753600,842006528,805306368,838860800,838860800,872415232,872415232,905969664,905969664,939524096,842530816,858783744,858783744))</Histogram>
<Selectivity>1</Selectivity>
</Property>
<Property name="outBaseEntity">
<AverageFieldSize>6.93</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" ANY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"),$lb(1,7,7,7,7,7,7,7,7,7,7,7,7,7,7),$lb(541150809,1095653632,1146441037,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,541349197))</Histogram>
<OutlierSelectivity>.966667:"dummy"</OutlierSelectivity>
<Selectivity>3.3333%</Selectivity>
</Property>
<Property name="outDataBody">
<Histogram>$lb(.06666666666666666667,1,0,$lb(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),$lb(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),$lb(805306368,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,805306368))</Histogram>
<Selectivity>3.3333%</Selectivity>
</Property>
<Property name="outEntity">
<AverageFieldSize>6.93</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," PID"),$lb(7,7,7,7,7,7,7,7,7,7,7,7,7,7,1),$lb(541349197,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1146441037,1346978816,542132548))</Histogram>
<OutlierSelectivity>.966667:"dummy"</OutlierSelectivity>
<Selectivity>3.3333%</Selectivity>
</Property>
<Property name="outProperty">
<AverageFieldSize>8.3</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," {""FORMAT"": ""INAOKA_PROGRAM_SAMPLE_SEMANTIC""}"),$lb(7,7,7,7,7,7,7,7,7,7,7,7,7,7,1),$lb(541349197,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1146441037,2065843791,544940614))</Histogram>
<OutlierSelectivity>.966667:"dummy"</OutlierSelectivity>
<Selectivity>3.3333%</Selectivity>
</Property>
<Property name="outRole">
<AverageFieldSize>7.17</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," SATURATION"),$lb(7,7,7,7,7,7,7,7,7,7,7,7,7,7,1),$lb(541349197,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1146441037,1396790357,542327124))</Histogram>
<OutlierSelectivity>.966667:"dummy"</OutlierSelectivity>
<Selectivity>3.3333%</Selectivity>
</Property>
<Property name="outSpatical">
<AverageFieldSize>6.93</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" ANY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"),$lb(1,7,7,7,7,7,7,7,7,7,7,7,7,7,7),$lb(541150809,1095653632,1146441037,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,541349197))</Histogram>
<OutlierSelectivity>.966667:"dummy"</OutlierSelectivity>
<Selectivity>3.3333%</Selectivity>
</Property>
<Property name="outTemporal">
<AverageFieldSize>6.93</AverageFieldSize>
<Histogram>$lb(.06666666666666666667,0,0,$lb(" ANY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"," DUMMY"),$lb(1,7,7,7,7,7,7,7,7,7,7,7,7,7,7),$lb(541150809,1095653632,1146441037,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,541349197))</Histogram>
<OutlierSelectivity>.966667:"dummy"</OutlierSelectivity>
<Selectivity>3.3333%</Selectivity>
</Property>
<SQLMap name="IDKEY">
<BlockCount>-4</BlockCount>
</SQLMap>
<StreamLocation>^FS.if30reS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
