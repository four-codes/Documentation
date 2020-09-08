    
    https://docs.microsoft.com/en-us/azure/role-based-access-control/change-history-report

    https://medium.com/faun/write-custom-logs-on-log-analytics-through-databricks-on-azure-68759dbeac55
    
    https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/

    https://docs.microsoft.com/en-us/azure/data-explorer/kql-quick-reference

    https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/tutorial?pivots=azuredataexplorer

    https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/best-practices

    https://cloudarchitected.com/2019/04/monitoring-azure-databricks/

    AzureActivity
    | where TimeGenerated > ago(60d) and Authorization contains "Microsoft.Authorization/roleAssignments"
    | summarize count() by bin(TimeGenerated, 1d), OperationName
    | render timechart


    AzureActivity
    | where TimeGenerated > ago(60d) and Authorization contains "Microsoft.Authorization/roleAssignments/write" and ActivityStatus == "Succeeded"
    | parse ResourceId with * "/providers/" TargetResourceAuthProvider "/" *
    | summarize count(), makeset(Caller) by TargetResourceAuthProvider

    Logs
    | where Level == "Critical"
    | count

    StormEvents 
    | where StartTime >= datetime(2007-11-01) and StartTime < datetime(2007-12-01)
    | where State == "FLORIDA"  
    | count 


    StormEvents
    | summarize event_count=count() by State
    | where event_count > 1800
    | project State, event_count
    | sort by event_count
    | render columnchart


    StormEvents
    | where State == "WASHINGTON" and StartTime >= datetime(2007-07-01) and StartTime <= datetime(2007-07-31)
    | summarize StormCount = count() by EventType
    | render piechart

    external_table("ArchivedProducts")   
    | where Timestamp > ago(365d)   
    | summarize Count=count() by ProductId,   
    | top 5 by Count


    let T1 = external_table("ArchivedProducts") |  where TimeStamp > ago(100d);   
    let T = Products; //T is an internal table   
    T1 | join T on ProductId | take 10


    StormEvents
    | take 5
    | project  StartTime, EndTime, EventType, State, EventNarrative  


    StormEvents
    | top 5 by StartTime desc
    | project  StartTime, EndTime, EventType, State, EventNarrative 

    StormEvents
    | sort by StartTime desc
    | take 5
    | project  StartTime, EndLat, EventType, EventNarrative


    StormEvents
    | limit 5
    | extend Duration = EndTime - StartTime 
    | project StartTime, EndTime, Duration, EventType, State


    print x=1
    | extend x = x + 1, y = x
    | extend x = x + 1


    StormEvents
    | summarize event_count = count() by State


    StormEvents 
    | summarize StormCount = count(), TypeOfStorms = dcount(EventType) by State
    | top 5 by StormCount desc



    StormEvents
    | where StartTime > datetime(2007-02-14) and StartTime < datetime(2007-02-21)
    | summarize event_count = count() by bin(StartTime, 1d)



    StormEvents 
    | summarize event_count=count(), mid = avg(BeginLat) by State 
    | sort by mid
    | where event_count > 1800
    | project State, event_count
    | render columnchart



    StormEvents
    | summarize event_count=count() by bin(StartTime, 1d)
    | render timechart



    StormEvents 
    | where StartTime > datetime(2007-06-04) and StartTime < datetime(2007-06-10) 
    | where Source in ("Source","Public","Emergency Manager","Trained Spotter","Law Enforcement")
    | summarize count() by bin(StartTime, 10h), Source


    StormEvents
    | extend hour = floor(StartTime % 1d , 1h)
    | summarize event_count=count() by hour
    | sort by hour asc
    | render timechart


    StormEvents
    | extend hour= floor( StartTime % 1d , 1h)
    | where State in ("GULF OF MEXICO","MAINE","VIRGINIA","WISCONSIN","NORTH DAKOTA","NEW JERSEY","OREGON")
    | summarize event_count=count() by hour, State
    | render timechart


    StormEvents
    | extend hour= floor( StartTime % 1d , 1h)/ 1h
    | where State in ("GULF OF MEXICO","MAINE","VIRGINIA","WISCONSIN","NORTH DAKOTA","NEW JERSEY","OREGON")
    | summarize event_count=count() by hour, State
    | render columnchart


    StormEvents
    | where EventType == "Lightning"
    | join (
        StormEvents 
        | where EventType == "Avalanche"
    ) on State  
    | distinct State


    Events
    | where eventName == "session_started"
    | project start_time = timestamp, stop_time, country, session_id
    | join ( Events
        | where eventName == "session_ended"
        | project stop_time = timestamp, session_id
        ) on session_id
    | extend duration = stop_time - start_time
    | project start_time, stop_time, country, duration
    | take 10


    StormEvents
    | extend  duration = EndTime - StartTime
    | where duration > 0s
    | where duration < 3h
    | summarize event_count = count()
        by bin(duration, 5m)
    | sort by duration asc
    | render timechart

    perf 
    | summarize percentiles(duration, 5, 20, 50, 80, 95)


    StormEvents
    | extend  duration = EndTime - StartTime
    | where duration > 0s
    | where duration < 3h
    | summarize event_count = count()
        by bin(duration, 5m), State
    | sort by duration asc
    | summarize percentiles(duration, 5, 20, 50, 80, 95) by State


    let LightningStorms = 
        StormEvents
        | where EventType == "Lightning";
    let AvalancheStorms = 
        StormEvents
        | where EventType == "Avalanche";
    LightningStorms 
    | join (AvalancheStorms) on State
    | distinct State


    StormEvents
    | where isnotempty(EndLocation) 
    | summarize event_count=count() by EndLocation
    | top 10 by event_count
    | render columnchart


    let Events = MyLogTable | where ... ;

    Events
    | where Name == "Start"
    | project Name, City, SessionId, StartTime=timestamp
    | join (Events 
            | where Name="Stop"
            | project StopTime=timestamp, SessionId) 
        on SessionId
    | project City, SessionId, StartTime, StopTime, Duration = StopTime - StartTime

    Events 
    | where Name == "Start" 
    | project City, ClientIp, StartTime = timestamp
    | join  kind=inner
        (Events
        | where Name == "Stop" 
        | project StopTime = timestamp, ClientIp)
        on ClientIp
    | extend duration = StopTime - StartTime 
        // Remove matches with earlier stops:
    | where  duration > 0  
        // Pick out the earliest stop for each start and client:
    | summarize arg_min(duration, *) by bin(StartTime,1s), ClientIp

    // Count the frequency of each duration:
        | summarize count() by duration=bin(min_duration/1s, 10) 
          // Cut off the long tail:
        | where duration < 300
          // Display in a bar chart:
        | sort by duration asc | render barchart
    


    Logs  
    | filter ActivityId == "ActivityId with Blablabla" 
    | summarize max(Timestamp), min(Timestamp)  
    | extend Duration = max_Timestamp - min_Timestamp 

    wabitrace  
    | filter Timestamp >= datetime(2015-01-12 11:00:00Z)  
    | filter Timestamp < datetime(2015-01-12 13:00:00Z)  
    | filter EventText like "NotifyHadoopApplicationJobPerformanceCounters"  	 
    | extend Tenant = extract("tenantName=([^,]+),", 1, EventText) 
    | extend Environment = extract("environmentName=([^,]+),", 1, EventText)  
    | extend UnitOfWorkId = extract("unitOfWorkId=([^,]+),", 1, EventText)  
    | extend TotalLaunchedMaps = extract("totalLaunchedMaps=([^,]+),", 1, EventText, typeof(real))  
    | extend MapsSeconds = extract("mapsMilliseconds=([^,]+),", 1, EventText, typeof(real)) / 1000 
    | extend TotalMapsSeconds = MapsSeconds  / TotalLaunchedMaps 
    | filter Tenant == 'DevDiv' and Environment == 'RollupDev2'  
    | filter TotalLaunchedMaps > 0 
    | summarize sum(TotalMapsSeconds) by UnitOfWorkId  
    | extend JobMapsSeconds = sum_TotalMapsSeconds * 1 
    | project UnitOfWorkId, JobMapsSeconds 
    | join ( 
    wabitrace  
    | filter Timestamp >= datetime(2015-01-12 11:00:00Z)  
    | filter Timestamp < datetime(2015-01-12 13:00:00Z)  
    | filter EventText like "NotifyHadoopApplicationJobPerformanceCounters"  
    | extend Tenant = extract("tenantName=([^,]+),", 1, EventText) 
    | extend Environment = extract("environmentName=([^,]+),", 1, EventText)  
    | extend UnitOfWorkId = extract("unitOfWorkId=([^,]+),", 1, EventText)   
    | extend TotalLaunchedReducers = extract("totalLaunchedReducers=([^,]+),", 1, EventText, typeof(real)) 
    | extend ReducesSeconds = extract("reducesMilliseconds=([^,]+)", 1, EventText, typeof(real)) / 1000 
    | extend TotalReducesSeconds = ReducesSeconds / TotalLaunchedReducers 
    | filter Tenant == 'DevDiv' and Environment == 'RollupDev2'  
    | filter TotalLaunchedReducers > 0 
    | summarize sum(TotalReducesSeconds) by UnitOfWorkId  
    | extend JobReducesSeconds = sum_TotalReducesSeconds * 1 
    | project UnitOfWorkId, JobReducesSeconds ) 
    on UnitOfWorkId 
    | join ( 
    wabitrace  
    | filter Timestamp >= datetime(2015-01-12 11:00:00Z)  
    | filter Timestamp < datetime(2015-01-12 13:00:00Z)  
    | filter EventText like "NotifyHadoopApplicationJobPerformanceCounters"  
    | extend Tenant = extract("tenantName=([^,]+),", 1, EventText) 
    | extend Environment = extract("environmentName=([^,]+),", 1, EventText)  
    | extend JobName = extract("jobName=([^,]+),", 1, EventText)  
    | extend StepName = extract("stepName=([^,]+),", 1, EventText)  
    | extend UnitOfWorkId = extract("unitOfWorkId=([^,]+),", 1, EventText)  
    | extend LaunchTime = extract("launchTime=([^,]+),", 1, EventText, typeof(datetime))  
    | extend FinishTime = extract("finishTime=([^,]+),", 1, EventText, typeof(datetime)) 
    | extend TotalLaunchedMaps = extract("totalLaunchedMaps=([^,]+),", 1, EventText, typeof(real))  
    | extend TotalLaunchedReducers = extract("totalLaunchedReducers=([^,]+),", 1, EventText, typeof(real)) 
    | extend MapsSeconds = extract("mapsMilliseconds=([^,]+),", 1, EventText, typeof(real)) / 1000 
    | extend ReducesSeconds = extract("reducesMilliseconds=([^,]+)", 1, EventText, typeof(real)) / 1000 
    | extend TotalMapsSeconds = MapsSeconds  / TotalLaunchedMaps  
    | extend TotalReducesSeconds = (ReducesSeconds / TotalLaunchedReducers / ReducesSeconds) * ReducesSeconds  
    | extend CalculatedDuration = (TotalMapsSeconds + TotalReducesSeconds) * time(1s) 
    | filter Tenant == 'DevDiv' and Environment == 'RollupDev2') 
    on UnitOfWorkId 
    | extend MapsFactor = TotalMapsSeconds / JobMapsSeconds 
    | extend ReducesFactor = TotalReducesSeconds / JobReducesSeconds 
    | extend CurrentLoad = 1536 + (768 * TotalLaunchedMaps) + (1536 * TotalLaunchedMaps) 
    | extend NormalizedLoad = 1536 + (768 * TotalLaunchedMaps * MapsFactor) + (1536 * TotalLaunchedMaps * ReducesFactor) 
    | summarize sum(CurrentLoad), sum(NormalizedLoad) by  JobName  
    | extend SaveFactor = sum_NormalizedLoad / sum_CurrentLoad

    X 
    | extend samples = range(bin(StartTime, 1m), StopTime, 1m)

    X 
    | mv-expand samples = range(bin(StartTime, 1m), StopTime , 1m)


    X
    | mv-expand samples = range(bin(StartTime, 1m), StopTime , 1m)
    | summarize count(SessionId) by bin(todatetime(samples),1m)

    let StartTime=ago(12h);
    let StopTime=now()
    T
    | where Timestamp > StartTime and Timestamp <= StopTime 
    | where ...
    | summarize Count=count() by bin(Timestamp, 5m)


    let StartTime=ago(12h);
    let StopTime=now()
    T
    | where Timestamp > StartTime and Timestamp <= StopTime 
    | summarize Count=count() by bin(Timestamp, 5m)
    | where ...
    | union ( // 1
      range x from 1 to 1 step 1 // 2
      | mv-expand Timestamp=range(StartTime, StopTime, 5m) to typeof(datetime) // 3
      | extend Count=0 // 4
      )
    | summarize Count=sum(Count) by bin(Timestamp, 5m) // 5


    Logs
    | where Timestamp >= datetime(2015-08-22) and Timestamp < datetime(2015-08-23) 
    | where Level == "e" and Service == "Inferences.UnusualEvents_Main" 
    | summarize count() by bin(Timestamp, 5min)
    | render anomalychart


    Logs
    | where Timestamp >= datetime(2015-08-22 05:00) and Timestamp < datetime(2015-08-22 06:00)
    | where Level == "e" and Service == "Inferences.UnusualEvents_Main"
    | summarize count() by Message 
    | top 10 by count_ 
    | project count_, Message


    Logs
    | where Timestamp >= datetime(2015-08-22 05:00) and Timestamp < datetime(2015-08-22 06:00)
    | where Level == "e" and Service == "Inferences.UnusualEvents_Main"
    | reduce by Message with threshold=0.35
    | project Count, Pattern


    Logs
    | where Timestamp >= datetime(2015-08-22 05:00) and Timestamp < datetime(2015-08-22 06:00)
    | where Level == "e" and Service == "Inferences.UnusualEvents_Main"
    | evaluate autocluster()





    // Data set definition
    let Source = datatable(DeviceModel:string, Count:long)
    [
      'iPhone5,1', 32,
      'iPhone3,2', 432,
      'iPhone7,2', 55,
      'iPhone5,2', 66,
    ];
    // Query start here
    let phone_mapping = dynamic(
      {
        "iPhone5,1" : "iPhone 5",
        "iPhone3,2" : "iPhone 4",
        "iPhone7,2" : "iPhone 6",
        "iPhone5,2" : "iPhone5"
      });
    Source 
    | project FriendlyName = phone_mapping[DeviceModel], Count





    // Create a query-time dimension table using datatable
    let DimTable = datatable(EventType:string, Code:string)
      [
        "Heavy Rain", "HR",
        "Tornado",    "T"
      ]
    ;
    DimTable
    | join StormEvents on EventType
    | summarize count() by Code


    // Create a query-time dimension table using datatable
    let TeamFoundationJobResult = datatable(Result:int, ResultString:string)
      [
        -1, 'None', 0, 'Succeeded', 1, 'PartiallySucceeded', 2, 'Failed',
        3, 'Stopped', 4, 'Killed', 5, 'Blocked', 6, 'ExtensionNotFound',
        7, 'Inactive', 8, 'Disabled', 9, 'JobInitializationError'
      ]
    ;
    JobHistory
      | where PreciseTimeStamp > ago(1h)
      | where Service  != "AX"
      | where Plugin has "Analytics"
      | sort by PreciseTimeStamp desc
      | join kind=leftouter TeamFoundationJobResult on Result
      | extend ExecutionTimeSpan = totimespan(ExecutionTime)
      | project JobName, StartTime, ExecutionTimeSpan, ResultString, ResultMessage
  
  
  
  
  
    let _start = datetime(2018-09-24);
    let _end = _start + 13d; 
    Fruits 
    | extend _bin = bin_at(Timestamp, 1d, _start) // #1 
    | extend _endRange = iif(_bin + 7d > _end, _end, 
                                iff( _bin + 7d - 1d < _start, _start,
                                    iff( _bin + 7d - 1d < _bin, _bin,  _bin + 7d - 1d)))  // #2
    | extend _range = range(_bin, _endRange, 1d) // #3
    | mv-expand _range to typeof(datetime) limit 1000000 // #4
    | summarize min(Price), max(Price), sum(Price) by Timestamp=bin_at(_range, 1d, _start) ,  Fruit // #5
    | where Timestamp >= _start + 7d; // #6



    A
    | extend A_Timestamp = Timestamp, Kind="A"
    | union (B | extend B_Timestamp = Timestamp, Kind="B")
    | order by ID, Timestamp asc 
    | extend t = iff(Kind == "A" and (prev(Kind) != "A" or prev(Id) != ID), 1, 0)
    | extend t = row_cumsum(t)
    | summarize Timestamp=make_list(Timestamp), EventB=make_list(EventB), arg_max(A_Timestamp, EventA) by t, ID
    | mv-expand Timestamp to typeof(datetime), EventB to typeof(string)
    | where isnotempty(EventB)
    | project-away t


    let _maxLookbackPeriod = 1m;  
    let _internalWindowBin = _maxLookbackPeriod / 2;
    let B_events = B 
        | extend ID = new_guid()
        | extend _time = bin(Timestamp, _internalWindowBin)
        | extend _range = range(_time - _internalWindowBin, _time + _maxLookbackPeriod, _internalWindowBin) 
        | mv-expand _range to typeof(datetime) 
        | extend B_Timestamp = Timestamp, _range;
    let A_events = A 
        | extend _time = bin(Timestamp, _internalWindowBin)
        | extend _range = range(_time - _internalWindowBin, _time + _maxLookbackPeriod, _internalWindowBin) 
        | mv-expand _range to typeof(datetime) 
        | extend A_Timestamp = Timestamp, _range;
    B_events
        | join kind=leftouter (
            A_events
    ) on ID, _range
    | where isnull(A_Timestamp) or (A_Timestamp <= B_Timestamp and B_Timestamp <= A_Timestamp + _maxLookbackPeriod)
    | extend diff = coalesce(B_Timestamp - A_Timestamp, _maxLookbackPeriod*2)
    | summarize arg_min(diff, *) by ID
    | project ID, B_Timestamp, A_Timestamp, EventB, EventA


    set query_results_cache_max_age = time(5m);
    GithubEvent
    | where CreatedAt > ago(180d)
    | summarize arg_max(CreatedAt, Type) by Id


    AzureDiagnostics
    | where Category  == "PipelineRuns" and State_s != "InProgress"
    | where ResourceProvider == "MICROSOFT.DATAFACTORY"

    ADFPipelineRun
    | where PipelineName =='roduced'
    | summarize count() by ResourceId

    ADFPipelineRun
    | where TimeGenerated < ago(1d) and PipelineName =='gestion_Produced'
    | summarize count() by PipelineName

    ADFPipelineRun
    | where TimeGenerated > ago(1d)

    ADFPipelineRun
    | where == 'Produced' and (Status contains "succeeded" or Status contains "failed")
    | summarize TimeGenerated  = max(TimeGenerated) by PipelineName,Start,End,Status
    | project PipelineName,TimeGenerated,Start,End,Status,Duration= End - Start
    | union (ADFPipelineRun
    | where PipelineName == 'roducts' and (Status contains "succeeded" or Status contains "failed"))
    | summarize TimeGenerated  = max(TimeGenerated) by PipelineName,Start,End,Status
    | project PipelineName,TimeGenerated,Start,End,Status,Duration= End - Start
    | union (ADFPipelineRun
    | where PipelineName == 'efine' and (Status contains "succeeded" or Status contains "failed"))
    | summarize TimeGenerated  = max(TimeGenerated) by PipelineName,Start,End,Status
    | project PipelineName,TimeGenerated,Start,End,Status,Duration= End - Start
    | union (ADFPipelineRun
    | where PipelineName == 'EFINE_FULL' and (Status contains "succeeded" or Status contains "failed"))
    | summarize TimeGenerated  = max(TimeGenerated) by PipelineName,Start,End,Status
    | project PipelineName,TimeGenerated,Start,End,Status,Duration= End - Start
    | union (ADFPipelineRun
    | where PipelineName == 'NCREMENTAL' and (Status contains "succeeded" or Status contains "failed"))
    | summarize TimeGenerated  = max(TimeGenerated) by PipelineName,Start,End,Status
    | project PipelineName,TimeGenerated,Start,End,Status,Duration= End - Start
    | union (ADFPipelineRun
    | where PipelineName == 'REFINE_FULL' and (Status contains "succeeded" or Status contains "failed"))
    | summarize TimeGenerated  = max(TimeGenerated) by PipelineName,Start,End,Status
    | project PipelineName,TimeGenerated,Start,End,Status,Duration= End - Start
    | union (ADFPipelineRun
    | where PipelineName == 'CREMENTAL' and (Status contains "succeeded" or Status contains "failed"))
    | summarize TimeGenerated  = max(TimeGenerated) by PipelineName,Start,End,Status
    | project PipelineName,TimeGenerated,Start,End,Status,Duration= End - Start
    | union (ADFPipelineRun
    | where PipelineName == 'Ffgg' and (Status contains "succeeded" or Status contains "failed"))
    | summarize TimeGenerated  = max(TimeGenerated) by PipelineName,Start,End,Status
    | project PipelineName,TimeGenerated,Start,End,Status,Duration= End - Start



    ADFActivityRun
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx" and Status == "Failed"
    | where PipelineName == "PL_DC_OBOA_DB_TO_PTReporting"
    | where TimeGenerated > ago(24h)
    | project PipelineName,TimeGenerated,Start,End,ErrorMessage
    | summarize by PipelineName

    ADFActivityRun
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx" and Status == "Failed"
    | where TimeGenerated > ago(24h)
    | summarize  by PipelineName

    ADFActivityRun
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx" and Status == "Failed"
    | where TimeGenerated > ago(24h)
    | project PipelineName,TimeGenerated,Start,End,ErrorMessage,ActivityName,ActivityType
    | summarize by PipelineName,ActivityName,ActivityType,ErrorMessage


    let data = ADFPipelineRun
    | where TimeGenerated > ago(2d)
    | where Status != "InProgress";
    data

    | summarize Count = count() by ResourceId, Status, PipelineName

    | join kind = inner
    (
    data
    | make-series Trend = count() default = 0 on TimeGenerated from ago(2d) to now() step 1h by ResourceId, Status, PipelineName
    | project-away TimeGenerated
    )
    on ResourceId, Status, PipelineName
    | project ResourceId, Count, Trend, Status, PipelineName
    | order by Count desc;


    let data = AzureDiagnostics
    | where TimeGenerated > ago(2d)
    | where status_s != "InProgress";
    data
    | summarize Count = count() by ResourceId, status_s, pipelineName_s
    | join kind = inner
    (
    data
    | make-series Trend = count() default = 0 on TimeGenerated from ago(2d) to now() step 1h by ResourceId, status_s, pipelineName_s
    | project-away TimeGenerated
    )
    on ResourceId, status_s, pipelineName_s
    | project ResourceId, Count, Trend, status_s, pipelineName_s
    | order by Count desc;


    let data = ADFPipelineRun
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx"
    | where TimeGenerated > startofday(now())
    | where Status != "InProgress";
    data
    | summarize Count = count() by ResourceId, Status, PipelineName
    | join kind = inner
    (
    data
    | make-series Trend = count() default = 0 on TimeGenerated from  startofday(now()) step 1h by ResourceId, Status, PipelineName
    | project-away TimeGenerated
    )
    on ResourceId, Status, PipelineName
    | project  Status, ResourceId, Count, Trend, PipelineName
    | order by Count desc
    | render piechart

    ADFActivityRun | where TimeGenerated > startofweek(now())
    ADFActivityRun | where TimeGenerated > startofday(now())

    let data = ADFPipelineRun
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx"
    | where TimeGenerated > startofday(now())
    | where Status != "InProgress";
    data
    | summarize Count = count() by ResourceId, Status, PipelineName
    | join kind = inner
    (
    data
    | make-series Trend = count() default = 0 on TimeGenerated from  startofday(now()) step 1h by ResourceId, Status, PipelineName
    | project-away TimeGenerated
    )
    on ResourceId, Status, PipelineName
    | project  Status, ResourceId, Count, Trend, PipelineName
    | order by Count desc
    | render piechart


    let data = ADFPipelineRun
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx"
    | where TimeGenerated > startofmonth(now())
    | where Status != "InProgress";
    data
    | summarize Count = count() by ResourceId, Status, PipelineName
    | join kind = inner
    (
    data
    | make-series Trend = count() default = 0 on TimeGenerated from  startofmonth(now()) step 1h by ResourceId, Status, PipelineName
    | project-away TimeGenerated
    )
    on ResourceId, Status, PipelineName
    | project  Status, ResourceId, Count, Trend, PipelineName
    | order by Count desc
    | render piechart


    ADFActivityRun
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx" and Status == "Failed"
    | where PipelineName == "eporting"
    | where TimeGenerated > ago(24h)
    | project Level

    ADFActivityRun
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx"
    | summarize count() by bin(TimeGenerated, 1d), PipelineName
    | render timechart

    ADFActivityRun
    | where TimeGenerated > ago(365d)
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx" and Status == "Failed"
    | summarize PipelineRunId=count() by PipelineName

    ADFActivityRun
    | where TimeGenerated > ago(365d)
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx" and Status == "Failed"
    | summarize PipelineRunId=count() by PipelineName
    | top 10 by PipelineName

    ADFActivityRun
    | where TimeGenerated > ago(365d)
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx" and Status == "Succeeded"
    | summarize PipelineRunId=count() by PipelineName
    | top 10 by PipelineName


    ADFActivityRun
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx" and Status == "Failed"
    | summarize PipelineRunId=count() by PipelineName
    | where TimeGenerated > ago(24h)
    | project PipelineName,PipelineRunId,TimeGenerated,Start,End,ErrorMessage,ActivityName,ActivityType
    | order by TimeGenerated



    ADFPipelineRun
    | where  TimeGenerated > ago(24h)
    | where ResourceId contains "xxxxxxxxxxxxxxxxxxxxx" and (Status contains "succeeded" or Status contains "failed")
    | summarize TimeGenerated  = max(TimeGenerated) by PipelineName,Start,End,Status
    | project PipelineName,TimeGenerated,Start,End,Status,Duration= End - Start
    | order by Duration asc


    StormEvents
    | limit 5
    | extend Duration = EndTime - StartTime
    | project StartTime, EndTime, Duration, EventType, State


    ADFPipelineRun
    | where ==  ResourceId contains "xxxxxxxxxxxxxxxxxxxxx" and (Status contains "succeeded" or Status contains "failed")
    | summarize TimeGenerated  = max(TimeGenerated) by PipelineName,Start,End,Status
    | project PipelineName,TimeGenerated,Start,End,Status,Duration= End - Start


    ADFPipelineRun
    | where  TimeGenerated > ago(24h)
    | where ResourceId contains "PNTDLUSSCT315TESTCVX" and (Status contains "succeeded" or Status contains "failed")
    | summarize TimeGenerated  = max(TimeGenerated) by PipelineName,Start,End,Status
    | project PipelineName,TimeGenerated,Start,End,Status,Duration= End - Start
    | order by TimeGenerated desc


    Important queries
    
    # PIPELINE RUNS BY DATA FACTORY

    let data = ADFPipelineRun
    | where TimeGenerated > ago(2d)
    | where Status != "InProgress";
    data
    | summarize Count = count() by ResourceId, Status, PipelineName
    | join kind = inner
    (
        data
        | make-series Trend = count()  default = 0 on TimeGenerated from ago(2d) to now() step 1h by ResourceId, Status, PipelineName
        | project-away TimeGenerated
    )
    on ResourceId, Status, PipelineName
    | project ResourceId, Count, Trend, Status, PipelineName
    | order by Count desc;


    #  ACTIVITY RUNS BY DATA FACTORY

    let data = ADFActivityRun
    | where TimeGenerated > ago(2d)
    | where Status != "InProgress";
    data
    | summarize Count = count() by ResourceId, Status, ActivityName
    | join kind = inner
    (
        data
        | make-series Trend = count()  default = 0 on TimeGenerated from ago(2d) to now() step 1h by ResourceId, Status, ActivityName
        | project-away TimeGenerated
    )
    on ResourceId, Status, ActivityName
    | project ResourceId, Count, Trend, Status, ActivityName
    | order by Count desc;


    # TRIGGER RUNS BY DATA FACTORY

    let data = ADFTriggerRun
    | where TimeGenerated > ago(2d)
    | where Status != "Running" and Status !contains "Waiting";
    data
    | summarize Count = count() by ResourceId, Status, TriggerName
    | join kind = inner
    (
        data
        | make-series Trend = count()  default = 0 on TimeGenerated from ago(2d) to now() step 1h by ResourceId, Status, TriggerName
        | project-away TimeGenerated
    )
    on ResourceId, Status, TriggerName
    | project ResourceId, Count, Trend, Status, TriggerName
    | order by Count desc;

    # TOP 10 PIPELINE ERRORS BY DATA FACTORY

    let data = ADFPipelineRun
    | where TimeGenerated > ago(2d)
    | where Status == "Failed";
    data
    | summarize Count = count() by ResourceId, FailureType, PipelineName
    | join kind = inner
    (
        data
        | make-series Trend = count()  default = 0 on TimeGenerated from ago(2d) to now() step 1h by ResourceId, FailureType, PipelineName
        | project-away TimeGenerated
    )
    on ResourceId, FailureType, PipelineName
    | project ResourceId, Count, Trend, FailureType, PipelineName
    | order by Count desc;

    # TOP 10 ACTIVITY ERRORS BY DATA FACTORY

    let data = ADFActivityRun
    | where TimeGenerated > ago(2d)
    | where Status == "Failed";
    data
    | summarize Count = count() by ResourceId, FailureType, ActivityName
    | join kind = inner
    (
        data
        | make-series Trend = count()  default = 0 on TimeGenerated from ago(2d) to now() step 1h by ResourceId, FailureType, ActivityName
        | project-away TimeGenerated
    )
    on ResourceId, FailureType, ActivityName
    | project ResourceId, Count, Trend, FailureType, ActivityName
    | order by Count desc;


    # TOP 10 TRIGGER ERRORS BY DATA FACTORY

    let data = ADFTriggerRun
    | where TimeGenerated > ago(2d)
    | where Status == "Failed";
    data
    | summarize Count = count() by ResourceId, TriggerName
    | join kind = inner
    (
        data
        | make-series Trend = count()  default = 0 on TimeGenerated from ago(2d) to now() step 1h by ResourceId, TriggerName
        | project-away TimeGenerated
    )
    on ResourceId, TriggerName
    | project ResourceId, Count, Trend, TriggerName
    | order by Count desc;


    # ACTIVITY RUNS BY TYPE

    let data = ADFActivityRun
    | where TimeGenerated > ago(2d)
    | where Status != "InProgress";
    data
    | summarize Count = count() by ResourceId, ActivityType
    | project ResourceId, ActivityType, Count
    | order by Count desc;


    #  TRIGGER RUNS BY TYPE


    let data = ADFTriggerRun
    | where TimeGenerated > ago(2d);
    data
    | summarize Count = count() by ResourceId, TriggerType, Status
    | project ResourceId, TriggerType, Status, Count
    | order by Count desc;


    # MAX PIPELINE RUNS DURATION

    let data = ADFPipelineRun
    | where TimeGenerated > ago(2d)
    | where Status != "InProgress"
    | extend DurationInMinutes = round((End - Start)/1m, 2) ;
    data
    | summarize Duration_Minutes = max(DurationInMinutes) by PipelineName
    | join kind = inner
    (
        data
        | make-series Trend = max(DurationInMinutes)  default = 0 on TimeGenerated from ago(2d) to now() step 1h by PipelineName
        | project-away TimeGenerated
    )
    on PipelineName
    | project PipelineName, Duration_Minutes, Trend
    | order by Duration_Minutes desc;






