function TodoFilter({setFilter}:any) {
    return (
        <div>
            <button className="btn btn-primary"onClick={()=>setFilter('all')}>All</button>
            <button onClick={()=>setFilter('active')} >Active</button>
            <button onClick={()=>setFilter('completed')}>Completed</button>
        </div>
    )
}

export default TodoFilter;