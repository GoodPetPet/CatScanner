import { useState } from 'react'
import TodoList from '@/components/TodoList'
import AddTodo from '@/components/AddTodo'
import TodoFilter from '@/components/TodoFilter'
import Test from '@/components/Test'
import { Todo } from '@types'

import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Flex } from 'antd';
import { SearchOutlined } from '@ant-design/icons';

import './App.css'
function App() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [filter, setFilter] = useState('all')


  const addTodo = (text: string) => {
    const newTodo: Todo = {
      id: Date.now(),
      text,
      completed: false
    }
    setTodos([...todos, newTodo])
  }

  const deleteTodo = (id: number) => {
   setTodos(todos.filter(todo => todo.id !== id))
  }

  const toggleTodo = (id: number) => {
    setTodos(todos.map(todo => {
      if (todo.id === id) {
        todo.completed = !todo.completed
      }
      return todo
    }))
  }
  const getFilteredTodos = () => {
    console.log('Current filter:', filter);
    switch (filter) {
      case 'completed':
        return todos.filter(todo => todo.completed)
      case 'active':
        return todos.filter(todo => !todo.completed)
      default:
        return todos
    }
  }

  return (
    <div>
      <nav className='navbar navbar-dark bg-primary'>
        hello world
      </nav>
      <h1 className='addTodo'>TodoList</h1>
      <AddTodo addTodo={addTodo}></AddTodo>
      <TodoList todos={getFilteredTodos()} deleteTodo={deleteTodo} toggleTodo={toggleTodo}></TodoList>
      <TodoFilter setFilter={setFilter}></TodoFilter>
      <button className="btn btn-success">Click Me</button>
      <Button icon={<SearchOutlined />} href="https://www.google.com" target="_blank">Search</Button>
      <Test></Test>
    </div>
  )
}

export default App
