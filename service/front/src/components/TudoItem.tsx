function TodoItem({todo,onToggleTodo,onDeleteTodo}:any) {
    return (
        <li style={{textDecoration:todo.completed ? 'line-through':'none'}}>
            { todo.text }
            <button onClick={() => onToggleTodo(todo.id)}>切换</button>
            <button onClick={() => onDeleteTodo(todo.id)}>删除</button>
        </li>
    )
}

export default TodoItem;
