Class vital.DeviceEntry Extends %Persistent
{

/// Description
Property deviceID As %String;

Property deviceType As %String;

ClassMethod Insert(DID As %String, DType As %String) As vital.DeviceEntry [ Language = python ]
{
    import iris
    newdata = iris.cls("vital.DeviceEntry")._New()
    newdata.deviceID = DID
    newdata.deviceType = DType
    stauts = newdata._Save()
    print(stauts)
}

ClassMethod getmaxID() As vital.DeviceEntry [ Language = python ]
{
    import iris
    statement = iris.sql.prepare("SELECT MAX(ID) FROM vital.DeviceEntry")
    rset = statement.execute()
    for row in rset:
        print(row)
    maxID = int(row[0])
    return maxID
}

ClassMethod existobject(id As %String) As %Status [ Language = objectscript ]
{
    Set eo = ##class(vital.DeviceEntry).%ExistsId(id)
    Return eo
}

Storage Default
{
<Data name="DeviceEntryDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>deviceID</Value>
</Value>
<Value name="3">
<Value>deviceType</Value>
</Value>
</Data>
<DataLocation>^vital.DeviceEntryD</DataLocation>
<DefaultData>DeviceEntryDefaultData</DefaultData>
<ExtentSize>3</ExtentSize>
<IdLocation>^vital.DeviceEntryD</IdLocation>
<IndexLocation>^vital.DeviceEntryI</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>1</Selectivity>
</Property>
<Property name="deviceID">
<AverageFieldSize>19</AverageFieldSize>
<Selectivity>33.3333%</Selectivity>
</Property>
<Property name="deviceType">
<AverageFieldSize>12.67</AverageFieldSize>
<Selectivity>33.3333%</Selectivity>
</Property>
<SQLMap name="IDKEY">
<BlockCount>-4</BlockCount>
</SQLMap>
<StreamLocation>^vital.DeviceEntryS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
