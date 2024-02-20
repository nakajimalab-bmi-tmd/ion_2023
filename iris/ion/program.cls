Class ion.program Extends %Persistent
{

Property outRole As %String;

Property outEntity As %String;

Property outBaseEntity As %String;

Property outDataBody As %Stream.GlobalBinary;

Property outTemporal As %String;

Property outSpatical As %String;

Property outProperty As %String;

ClassMethod InsertNewpy(R As %String, E As %String, BE As %String, DB As %Binary, T As %String, S As %String, P As %String) As ion.program [ Language = python ]
{
    import iris

    newdata = iris.cls("ion.program")._New()
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

ClassMethod InsertAddpy(DB As %Binary, id As %String) As ion.program [ Language = python ]
{
    import iris
    #print(len(data))
    add = iris.cls("ion.program")._OpenId(id)

   
    add.outDataBody.MoveToEnd()

    add.outDataBody.Write(data)
    
    status = add._Save()
    #print(add.ImageData.Size)
    return status
}

ClassMethod getprogrampy(id As %String, step As %Binary, pos As %Binary) As ion.program [ Language = python ]
{
    import iris
    result = iris.cls("ion.program")._OpenId(id)
    #print(result.ImageData.Size)
    result.outDataBody.MoveTo(pos)
    #; while len(bin) < result.outDataBody.Size:
    #;     bin = bin + result.outDataBody.Read(step)
    bin = result.outDataBody.Read(step)
    
    return bin
}

ClassMethod existobject(id As %String) As %Status [ Language = objectscript ]
{
    Set eo = ##class(ion.program).%ExistsId(id)
    Return eo
}

ClassMethod getmaxID() As ion.program [ Language = python ]
{
    import iris
    statement = iris.sql.prepare("SELECT MAX(ID) FROM ion.program")
    rset = statement.execute()
    for row in rset:
        row
    maxID = int(row[0])
    return maxID
}

ClassMethod delobject(id As %String) As %Status [ Language = objectscript ]
{
    Set sc = ##class(ion.program).%DeleteId(id)
    return sc
}

ClassMethod ChangeProperty(numID As %String, prp As %String) As ion.program [ Language = python ]
{
    import iris

    changedata = iris.cls("ion.program")._OpenId(numID)
    changedata.outProperty = prp
    status = changedata._Save()
    return status
}

Storage Default
{
<Data name="programDefaultData">
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
<DataLocation>^ion.programD</DataLocation>
<DefaultData>programDefaultData</DefaultData>
<ExtentSize>1</ExtentSize>
<IdLocation>^ion.programD</IdLocation>
<IndexLocation>^ion.programI</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>1</Selectivity>
</Property>
<Property name="outBaseEntity">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outDataBody">
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outEntity">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outProperty">
<AverageFieldSize>39</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outRole">
<AverageFieldSize>5</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outSpatical">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outTemporal">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<SQLMap name="IDKEY">
<BlockCount>-4</BlockCount>
</SQLMap>
<StreamLocation>^ion.programS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
