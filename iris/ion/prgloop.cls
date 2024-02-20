Class ion.prgloop Extends %Persistent
{

Property outRole As %String;

Property outEntity As %String;

Property outBaseEntity As %String;

Property outDataBody As %Stream.GlobalBinary;

Property outTemporal As %String;

Property outSpatical As %String;

Property outProperty As %String;

ClassMethod InsertNewpy(R As %String, E As %String, BE As %String, DB As %Binary, T As %String, S As %String, P As %String) As ion.prgloop [ Language = python ]
{
    import iris

    newdata = iris.cls("ion.prgloop")._New()
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

ClassMethod InsertAddpy(DB As %Binary, id As %String) As ion.prgloop [ Language = python ]
{
    import iris
    #print(len(data))
    add = iris.cls("ion.prgloop")._OpenId(id)

   
    add.outDataBody.MoveToEnd()

    add.outDataBody.Write(data)
    
    status = add._Save()
    #print(add.ImageData.Size)
    return status
}

ClassMethod getprogrampy(id As %String, step As %Binary, pos As %Binary) As ion.prgloop [ Language = python ]
{
    import iris
    result = iris.cls("ion.prgloop")._OpenId(id)
    #print(result.ImageData.Size)
    result.outDataBody.MoveTo(pos)
    #; while len(bin) < result.outDataBody.Size:
    #;     bin = bin + result.outDataBody.Read(step)
    bin = result.outDataBody.Read(step)
    
    return bin
}

ClassMethod existobject(id As %String) As %Status [ Language = objectscript ]
{
    Set eo = ##class(ion.prgloop).%ExistsId(id)
    Return eo
}

ClassMethod getmaxID() As ion.prgloop [ Language = python ]
{
    import iris
    statement = iris.sql.prepare("SELECT MAX(ID) FROM ion.prgloop")
    rset = statement.execute()
    for row in rset:
        row
    maxID = int(row[0])
    return maxID
}

ClassMethod delobject(id As %String) As %Status [ Language = objectscript ]
{
    Set sc = ##class(ion.prgloop).%DeleteId(id)
    return sc
}

ClassMethod ChangeProperty(numID As %String, prp As %String) As ion.prgloop [ Language = python ]
{
    import iris

    changedata = iris.cls("ion.prgloop")._OpenId(numID)
    changedata.outProperty = prp
    status = changedata._Save()
    return status
}

Storage Default
{
<Data name="prgloopDefaultData">
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
<DataLocation>^ion.prgloopD</DataLocation>
<DefaultData>prgloopDefaultData</DefaultData>
<ExtentSize>2</ExtentSize>
<IdLocation>^ion.prgloopD</IdLocation>
<IndexLocation>^ion.prgloopI</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>1</Selectivity>
</Property>
<Property name="outBaseEntity">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outDataBody">
<Selectivity>50.0000%</Selectivity>
</Property>
<Property name="outEntity">
<AverageFieldSize>5</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="outProperty">
<AverageFieldSize>41</AverageFieldSize>
<Selectivity>50.0000%</Selectivity>
</Property>
<Property name="outRole">
<AverageFieldSize>7</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
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
<StreamLocation>^ion.prgloopS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
