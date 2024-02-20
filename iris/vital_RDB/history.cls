Class vital.history Extends %Persistent
{

Property historyID As %String;

Property PID As %String;

Property NID As %String;

Property deviceID As %String;

Property useTime As %String;

ClassMethod Insert(HID As %String, patient As %String, nurse As %String, DID As %String, UT As %String) As vital.history [ Language = python ]
{
    import iris
    newdata = iris.cls("vital.history")._New()
    newdata.historyID = HID
    newdata.PID = patient
    newdata.NID = nurse
    newdata.deviceID = DID
    newdata.useTime = UT
    stauts = newdata._Save()
    print(stauts)
    return stauts
}

ClassMethod ChangeNID(numID As %String, nurse As %String) As vital.history [ Language = python ]
{
    import iris

    changedata = iris.cls("vital.history")._OpenId(numID)
    changedata.NID = nurse
    status = changedata._Save()
    return status
}

ClassMethod getmaxID() As vital.history [ Language = python ]
{
    import iris
    statement = iris.sql.prepare("SELECT MAX(ID) FROM vital.history")
    rset = statement.execute()
    for row in rset:
        print(row)
    maxID = row[0]
    return maxID
}

ClassMethod existobject(id As %String) As %Status [ Language = objectscript ]
{
    Set eo = ##class(vital.history).%ExistsId(id)
    Return eo
}

Storage Default
{
<Data name="historyDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>historyID</Value>
</Value>
<Value name="3">
<Value>PID</Value>
</Value>
<Value name="4">
<Value>Entity</Value>
</Value>
<Value name="5">
<Value>baseEntity</Value>
</Value>
<Value name="6">
<Value>deviceID</Value>
</Value>
<Value name="7">
<Value>usetTime</Value>
</Value>
<Value name="8">
<Value>useTime</Value>
</Value>
<Value name="9">
<Value>NID</Value>
</Value>
</Data>
<DataLocation>^vital.historyD</DataLocation>
<DefaultData>historyDefaultData</DefaultData>
<ExtentSize>1</ExtentSize>
<IdLocation>^vital.historyD</IdLocation>
<IndexLocation>^vital.historyI</IndexLocation>
<Property name="%%CLASSNAME">
<AverageFieldSize>2</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="%%ID">
<AverageFieldSize>3</AverageFieldSize>
<Selectivity>1</Selectivity>
</Property>
<Property name="PID">
<AverageFieldSize>8</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="deviceID">
<AverageFieldSize>19</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="historyID">
<AverageFieldSize>11</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<Property name="useTime">
<AverageFieldSize>28</AverageFieldSize>
<Selectivity>100.0000%</Selectivity>
</Property>
<SQLMap name="IDKEY">
<BlockCount>-4</BlockCount>
</SQLMap>
<StreamLocation>^vital.historyS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
