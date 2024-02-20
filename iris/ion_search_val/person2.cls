Class FS.person2 Extends %Persistent
{

Property json As %Stream.GlobalCharacter;

Property str As %String;

/// Description
ClassMethod jsoninsert(j As %String, s As %String) As FS.person2 [ Language = objectscript ]
{
    Set person = ##class(FS.person2).%New()  
    ///set person.json = {}.%FromJSON(j.%ToJSON())
    do person.json.Write(j)
    ///write person.json
    set person.str = s
    set sc = person.%Save()
    Return sc
}

ClassMethod jsonget(id As %String) As FS.person2 [ Language = objectscript ]
{
    Set object = ##class(FS.person2).%OpenId(id)  
    Do object.json.Rewind() 
    While (object.json.AtEnd = 0) {
        Set len = object.json.Size
        ///Write result.ImageData.Read(.len)
        ///set str = result.ImageData.Read()
        set bin = object.json.Read(.len)
    }
    return bin
}

Storage Default
{
<Data name="json">
<Attribute>json</Attribute>
<Structure>node</Structure>
<Subscript>"json"</Subscript>
</Data>
<Data name="person2DefaultData">
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
<Value>str</Value>
</Value>
</Data>
<DataLocation>^FS.person2D</DataLocation>
<DefaultData>person2DefaultData</DefaultData>
<ExtentSize>2</ExtentSize>
<IdLocation>^FS.person2D</IdLocation>
<IndexLocation>^FS.person2I</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>1</Selectivity>
</Property>
<Property name="json">
<Selectivity>50.0000%</Selectivity>
</Property>
<Property name="str">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<SQLMap name="IDKEY">
<BlockCount>-4</BlockCount>
</SQLMap>
<StreamLocation>^FS.person2S</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
