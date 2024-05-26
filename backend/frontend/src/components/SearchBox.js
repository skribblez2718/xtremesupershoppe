
import React, { useState } from 'react'
import { Button, Form, Row, Col, InputGroup } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'

function SearchBox() {
    const [keyword, setKeyword] = useState('')

    let history = useHistory()

    const submitHandler = (e) => {
        e.preventDefault()
        if (keyword) {
            history.push(`/?keyword=${keyword}&page=1`)
        } else {
            history.push(history.push(history.location.pathname))
        }
    }
    return (
        <Form onSubmit={submitHandler} inline>
            <Row>
                <Form.Group as={Col} controlId="search">
                    <InputGroup>
                        <Button
                            type='submit'
                            className='p-2'
                            onClick={submitHandler}
                        >
                            <i class="fa fa-search"></i>
                        </Button>
                        <Form.Control
                            type='text'
                            name='q'
                            onChange={(e) => setKeyword(e.target.value)}
                            className='mr-sm-2 ml-sm-5'
                            placeholder="Search..."
                        />
                    </InputGroup>
                </Form.Group>
            </Row>
        </Form>
    )
}

export default SearchBox