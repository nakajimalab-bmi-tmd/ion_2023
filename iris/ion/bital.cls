Class ion.bital Extends %Persistent
{

Property Role As %String;

Property Entity As %String;

Property baseEntity As %String;

Property databody As %Binary;

Property Temporal As %String;

Property Spatical As %String;

Property propety As %String;

ClassMethod Insert(R As %String, E As %String, BE As %String, DB As %Binary, T As %String, S As %String, P As %String) As ion.bital [ Language = python ]
{
    import iris
    newdata = iris.cls("ion.bital")._New()
    newdata.Role = R
    newdata.Entity = E
    newdata.baseEntity = BE
    newdata.databody = DB
    newdata.Temporal = T
    newdata.Spatical = S
    newdata.propety = P
    stauts = newdata._Save()
    return stauts
}

ClassMethod ChangeDB(id As %String, DB As %Binary) As ion.bital [ Language = python ]
{
    import iris
    chdata = iris.cls("ion.bital")._OpenId(id)
    chdata.databody = DB
    stauts = chdata._Save()
    return stauts
}

ClassMethod ChangeProperty(id As %String, p As %String) As ion.bital [ Language = python ]
{
    import iris
    chdata = iris.cls("ion.bital")._OpenId(id)
    chdata.propety = p
    stauts = chdata._Save()
    return stauts
}

ClassMethod ChangeRole(id As %String, r As %String) As ion.bital [ Language = python ]
{
    import iris
    chdata = iris.cls("ion.bital")._OpenId(id)
    chdata.Role = r
    stauts = chdata._Save()
    return stauts
}

ClassMethod getDB(id As %String) As ion.bital [ Language = objectscript ]
{
    Set person = ##class(ion.bital).%OpenId(id)
    Return person.databody
}

ClassMethod getRole(id As %String) As ion.bital [ Language = objectscript ]
{
    Set person = ##class(ion.bital).%OpenId(id)
    Return person.Role
}

ClassMethod getEntity(id As %String) As ion.bital [ Language = objectscript ]
{
    Set person = ##class(ion.bital).%OpenId(id)
    Return person.Entity
}

ClassMethod getBE(id As %String) As ion.bital [ Language = objectscript ]
{
    Set person = ##class(ion.bital).%OpenId(id)
    Return person.baseEntity
}

ClassMethod getTemporal(id As %String) As ion.bital [ Language = objectscript ]
{
    Set person = ##class(ion.bital).%OpenId(id)
    Return person.Temporal
}

ClassMethod getRoleEntity(R As %String, E As %String) As ion.bital [ Language = python ]
{
    import iris
    maxID = iris.cls("ion.bital").getmaxID()

    for i in range(1,maxID):
        EO = iris.cls("ion.bital").existobject(str(i))
        if EO == 1:
            object = iris.cls("ion.bital")._OpenId(str(i))
            if object.Role == R and object.Entity == E:
                DB =  object.databody
                break
    
    return DB
}

ClassMethod getSpatical(id As %String) As ion.bital [ Language = objectscript ]
{
    Set person = ##class(ion.bital).%OpenId(id)
    Return person.Spatical
}

ClassMethod delobject(id As %String) As %Status [ Language = objectscript ]
{
    Set sc = ##class(ion.bital).%DeleteId(id)
    Return sc
}

ClassMethod existobject(id As %String) As %Status [ Language = objectscript ]
{
    Set eo = ##class(ion.bital).%ExistsId(id)
    Return eo
}

ClassMethod getmaxID() As FS.Person [ Language = python ]
{
    import iris
    statement = iris.sql.prepare("SELECT MAX(ID) FROM ion.bital")
    rset = statement.execute()
    for row in rset:
        row
    maxID = int(row[0])
    return maxID
}

Storage Default
{
<Data name="bitalDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>Role</Value>
</Value>
<Value name="3">
<Value>Entity</Value>
</Value>
<Value name="4">
<Value>baseEntity</Value>
</Value>
<Value name="5">
<Value>databody</Value>
</Value>
<Value name="6">
<Value>Temporal</Value>
</Value>
<Value name="7">
<Value>Spatical</Value>
</Value>
<Value name="8">
<Value>propety</Value>
</Value>
</Data>
<DataLocation>^ion.bitalD</DataLocation>
<DefaultData>bitalDefaultData</DefaultData>
<ExtentSize>6</ExtentSize>
<IdLocation>^ion.bitalD</IdLocation>
<IndexLocation>^ion.bitalI</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>1</Selectivity>
</Property>
<Property name="Entity">
<AverageFieldSize>8</AverageFieldSize>
<Selectivity>50.0000%</Selectivity>
</Property>
<Property name="Role">
<AverageFieldSize>10</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="Spatical">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="Temporal">
<AverageFieldSize>28</AverageFieldSize>
<Selectivity>33.3333%</Selectivity>
</Property>
<Property name="baseEntity">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="databody">
<AverageFieldSize>19</AverageFieldSize>
<Selectivity>33.3333%</Selectivity>
</Property>
<Property name="propety">
<Selectivity>100.0000%</Selectivity>
</Property>
<SQLMap name="IDKEY">
<BlockCount>-4</BlockCount>
</SQLMap>
<StreamLocation>^ion.bitalS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
