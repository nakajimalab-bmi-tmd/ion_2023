Class FS.Person Extends %Persistent
{

/// Description
Property Name As %String;

Property DOB As %Date;

Property bin As %Binary;

/// Index NameID On Name [ Unique ];
/// Description
ClassMethod Insert(n As %String, bina As %SYS.Python = "null") As FS.Person [ Language = objectscript ]
{
    Set person = ##class(FS.Person).%New()
    Set person.Name = n
    ///Set person.DOB = $System.SQL.(dob, "YYYY/MM/DD")
    set person.bin = ##class(%SYS.Python).Bytes(bina)
    zwrite bina
    zwrite person.Name
    zwrite person.bin
    set sc = person.%Save()
    Return sc
}

ClassMethod Insertpy(n As %String, bina As %Binary = "null") As FS.Person [ Language = python ]
{
    import iris

    person = iris.cls("FS.Person")._New()

    person.Name = n
    person.bin = bina

    status = person._Save()

    return status
}

ClassMethod getbin(id As %String) As %Binary [ Language = objectscript ]
{
    Set person = ##class(FS.Person).%OpenId(id)
    set gb = ##class(%SYS.Python).Bytes(person.bin)
    zwrite gb
    zwrite gb."__getitem__"(0)
    ///Set binary = ##class(%Binary).%New()
    ///Do person.bin.OutputToDevice(binary)
    ///Set binaryStream = ##class(%Stream.GlobalBinary).%New()
    ///Set binaryData = person.bin.Read()
    Return gb
}

ClassMethod getbinpy(id As %String) As %Binary [ Language = python ]
{
    import iris
    person = iris.cls("FS.Person")._OpenId(id)

    return person.bin
}

ClassMethod getName(id As %String) As FS.Person [ Language = objectscript ]
{
    Set person = ##class(FS.Person).%OpenId(id)
    Return person.Name
}

ClassMethod getallpy(id As %String) As FS.Person [ Language = python ]
{
    import iris

    person = iris.cls("FS.Person")._OpenId(id)
    ls = [person.Name, person.bin]
    
    return ls
}

ClassMethod getallos(id As %String) As %SYS.Python [ Language = objectscript ]
{
    set p = ##class(FS.Person).%OpenId(id)
    set ls = $LISTBUILD(p.Name, p.bin)
    set pyls = ##class(%SYS.Python).Builtins().list()
    do pyls.append(p.Name)
    do pyls.append(p.bin)
    zwrite pyls
    return ls
}

ClassMethod getDOB(id As %String) As FS.Person [ Language = objectscript ]
{
    Set person = ##class(FS.Person).%OpenId(id)
    Return person.DOB
}

ClassMethod getindex(n As %String) As FS.Person [ Language = objectscript ]
{
    SET name = ##class(FS.Person).NameIDOpen(n)
    return name.Name
}

ClassMethod delobject(id As %String) As %Status [ Language = objectscript ]
{
    Set sc = ##class(FS.Person).%DeleteId(id)
    return sc
}

ClassMethod getmaxID() As FS.Person [ Language = python ]
{
    import iris
    statement = iris.sql.prepare("SELECT MAX(ID) FROM FS.Person")
    rset = statement.execute()
    for row in rset:
        print(row)
    maxID = int(row[0])
    return maxID
}

Storage Default
{
<Data name="PersonDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>Name</Value>
</Value>
<Value name="3">
<Value>DOB</Value>
</Value>
<Value name="4">
<Value>bin</Value>
</Value>
</Data>
<DataLocation>^FS.PersonD</DataLocation>
<DefaultData>PersonDefaultData</DefaultData>
<ExtentSize>1</ExtentSize>
<IdLocation>^FS.PersonD</IdLocation>
<IndexLocation>^FS.PersonI</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>1</Selectivity>
</Property>
<Property name="DOB">
<AverageFieldSize>4</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="Name">
<AverageFieldSize>8</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<SQLMap name="IDKEY">
<BlockCount>-4</BlockCount>
</SQLMap>
<StreamLocation>^FS.PersonS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
