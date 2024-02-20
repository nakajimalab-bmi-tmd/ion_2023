Class FS.practice Extends %Persistent
{

Property ImageData As %Stream.GlobalBinary;

ClassMethod Insert(data As %Binary) As FS.practice [ Language = objectscript ]
{
    Set newdata = ##class(FS.practice).%New()
    ///set newdata.ImageData = data
    do data.Rewind()
    while (data.AtEnd = 0){
        set len = 5000
        set r = data.Read(.len)
    }
    //do newdata.ImageData.Write(r)
    ///do newdata.ImageData.Write(data)
    //set sc = newdata.%Save()
    //Return sc
}

ClassMethod Insertos(data As %Binary) As FS.practice [ Language = objectscript ]
{
    #; Set newdata = ##class(FS.practice).%New()
    #; set strdata = ##class(%SYS.Python).Builtins().str(data)
    Return data
}

ClassMethod InsertNewpy(data As %Binary) As FS.practice [ Language = python ]
{
    import iris

    newdata = iris.cls("FS.practice")._New()
    
    newdata.ImageData.MoveToEnd()

    newdata.ImageData.Write(data)
    
    status = newdata._Save()
    id = newdata._Id()
    return id
}

ClassMethod InsertAddpy(data As %Binary, id As %String) As FS.practice [ Language = python ]
{
    import iris
    #print(len(data))
    add = iris.cls("FS.practice")._OpenId(id)

   
    add.ImageData.MoveToEnd()

    add.ImageData.Write(data)
    
    status = add._Save()
    #print(add.ImageData.Size)
    return status
}

ClassMethod getdata(id As %String) As FS.practice [ Language = objectscript ]
{
    Set result = ##class(FS.practice).%OpenId(id)
    set str = ""
    #; Do result.ImageData.Rewind() 
    While (result.ImageData.AtEnd = 0) {
        Set len = result.ImageData.Size
        set bin = result.ImageData.Read(len)
    }
    return bin
}

ClassMethod getdatapy(id As %String, step As %Binary, pos As %Binary) As FS.practice [ Language = python ]
{
    import iris
    result = iris.cls("FS.practice")._OpenId(id)
    #print(result.ImageData.Size)
    result.ImageData.MoveTo(pos)
    #; while len(bin) < result.ImageData.Size:
    #;     bin = bin + result.ImageData.Read(step)
    bin = result.ImageData.Read(step)
    
    return bin
}

ClassMethod delobject(id As %String) As %Status [ Language = objectscript ]
{
    Set sc = ##class(FS.practice).%DeleteId(id)
    Return sc
}

Storage Default
{
<Data name="practiceDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>pics</Value>
</Value>
<Value name="3">
<Value>ImageData</Value>
</Value>
</Data>
<DataLocation>^FS.practiceD</DataLocation>
<DefaultData>practiceDefaultData</DefaultData>
<ExtentSize>1</ExtentSize>
<IdLocation>^FS.practiceD</IdLocation>
<IndexLocation>^FS.practiceI</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>1</Selectivity>
</Property>
<Property name="ImageData">
<Selectivity>100.0000%</Selectivity>
</Property>
<SQLMap name="IDKEY">
<BlockCount>-4</BlockCount>
</SQLMap>
<StreamLocation>^FS.practiceS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
