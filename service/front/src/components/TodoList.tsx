import { Todo }from "@types"
import TodoItem from "./TudoItem";

interface TodoListProps {
    todos:Array<Todo>;
    toggleTodo:(id:number) => void;
    deleteTodo:(id:number) => void;
}


function TodoList({todos,toggleTodo,deleteTodo}:TodoListProps) {
    return (
        <ul>
            {todos.map((todo) => (
                <TodoItem key={todo.id} todo={todo} onToggleTodo={toggleTodo} onDeleteTodo={deleteTodo} />
                ))}
        </ul>
    )
}

export default TodoList;
