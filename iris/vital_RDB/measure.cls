Class vital.measure Extends %Persistent
{

Property measureID As %String;

Property deviceID As %String;

Property vitalname As %String;

Property value As %Binary;

Property Time As %String;

ClassMethod Insert(MID As %String, DID As %String, VN As %String, V As %Binary, UT As %String) As vital.measure [ Language = python ]
{
    import iris
    newdata = iris.cls("vital.measure")._New()
    newdata.measureID = MID
    newdata.deviceID = DID
    newdata.vitalname = VN
    newdata.value = V
    newdata.Time = UT
    stauts = newdata._Save()
    print(stauts)
    return stauts
}

ClassMethod getmaxID() As vital.measure [ Language = python ]
{
    import iris
    statement = iris.sql.prepare("SELECT MAX(ID) FROM vital.measure")
    rset = statement.execute()
    for row in rset:
        print(row)
    maxID = row[0]
    return maxID
}

ClassMethod ChangeMID(numID As %String, M As %String) As vital.measure [ Language = python ]
{
    import iris

    changedata = iris.cls("vital.measure")._OpenId(numID)
    changedata.measureID = M
    status = changedata._Save()
    return status
}

ClassMethod Changevalue(numID As %String, V As %String) As vital.measure [ Language = python ]
{
    import iris

    changedata = iris.cls("vital.measure")._OpenId(numID)
    changedata.value = V
    status = changedata._Save()
    return status
}

ClassMethod existobject(id As %String) As %Status [ Language = objectscript ]
{
    Set eo = ##class(vital.measure).%ExistsId(id)
    Return eo
}

Storage Default
{
<Data name="measureDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>measureID</Value>
</Value>
<Value name="3">
<Value>deviceID</Value>
</Value>
<Value name="4">
<Value>vitalname</Value>
</Value>
<Value name="5">
<Value>value</Value>
</Value>
<Value name="6">
<Value>Time</Value>
</Value>
</Data>
<DataLocation>^vital.measureD</DataLocation>
<DefaultData>measureDefaultData</DefaultData>
<ExtentSize>1</ExtentSize>
<IdLocation>^vital.measureD</IdLocation>
<IndexLocation>^vital.measureI</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>1</Selectivity>
</Property>
<Property name="Time">
<AverageFieldSize>28</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="deviceID">
<AverageFieldSize>19</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="measureID">
<AverageFieldSize>11</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="value">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="vitalname">
<AverageFieldSize>12</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<SQLMap name="IDKEY">
<BlockCount>-4</BlockCount>
</SQLMap>
<StreamLocation>^vital.measureS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
