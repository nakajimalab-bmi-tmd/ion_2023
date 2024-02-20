Class FS.if5 Extends %Persistent
{

Property outRole As %String;

Property outEntity As %String;

Property outBaseEntity As %String;

Property outDataBody As %Stream.GlobalBinary;

Property outTemporal As %String;

Property outSpatical As %String;

Property outProperty As %String;

ClassMethod InsertNewpy(R As %String, E As %String, BE As %String, DB As %Binary, T As %String, S As %String, P As %String) As FS.if5 [ Language = python ]
{
    import iris

    newdata = iris.cls("FS.if5")._New()
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

ClassMethod InsertAddpy(DB As %Binary, id As %String) As FS.if5 [ Language = python ]
{
    import iris
    #print(len(data))
    add = iris.cls("FS.if5")._OpenId(id)

   
    add.outDataBody.MoveToEnd()

    add.outDataBody.Write(data)
    
    status = add._Save()
    #print(add.ImageData.Size)
    return status
}

ClassMethod getprogrampy(id As %String, step As %Binary, pos As %Binary) As FS.if5 [ Language = python ]
{
    import iris
    result = iris.cls("FS.if5")._OpenId(id)
    #print(result.ImageData.Size)
    result.outDataBody.MoveTo(pos)
    #; while len(bin) < result.outDataBody.Size:
    #;     bin = bin + result.outDataBody.Read(step)
    bin = result.outDataBody.Read(step)
    
    return bin
}

ClassMethod existobject(id As %String) As %Status [ Language = objectscript ]
{
    Set eo = ##class(FS.if5).%ExistsId(id)
    Return eo
}

ClassMethod getmaxID() As FS.if5 [ Language = python ]
{
    import iris
    statement = iris.sql.prepare("SELECT MAX(ID) FROM FS.if5")
    rset = statement.execute()
    for row in rset:
        row
    maxID = int(row[0])
    return maxID
}

ClassMethod delobject(id As %String) As %Status [ Language = objectscript ]
{
    Set sc = ##class(FS.if5).%DeleteId(id)
    return sc
}

Storage Default
{
<Data name="if5DefaultData">
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
<DataLocation>^FS.if5D</DataLocation>
<DefaultData>if5DefaultData</DefaultData>
<ExtentSize>5</ExtentSize>
<IdLocation>^FS.if5D</IdLocation>
<IndexLocation>^FS.if5I</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>1</Selectivity>
</Property>
<Property name="outBaseEntity">
<AverageFieldSize>5</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outDataBody">
<Selectivity>20.0000%</Selectivity>
</Property>
<Property name="outEntity">
<AverageFieldSize>5</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outProperty">
<AverageFieldSize>37</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outRole">
<AverageFieldSize>12.4</AverageFieldSize>
<Selectivity>20.0000%</Selectivity>
</Property>
<Property name="outSpatical">
<AverageFieldSize>5</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outTemporal">
<AverageFieldSize>5</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<SQLMap name="IDKEY">
<BlockCount>-4</BlockCount>
</SQLMap>
<StreamLocation>^FS.if5S</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
