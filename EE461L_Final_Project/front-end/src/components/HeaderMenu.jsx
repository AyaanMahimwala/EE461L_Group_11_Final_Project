import React from 'react'
import { Box, Button, HStack, Heading, Flex, Spacer } from '@chakra-ui/react'
import { Link } from 'react-router-dom'


export default function HeaderMenu() {
    return (
        <Flex m="4">
            <Box>
                <Heading>EE461L Final Project!</Heading>
            </Box>
            <Spacer />
            <Box>
                <HStack>
                    <Link to='/'>
                        <Button variant="ghost">Home</Button>
                    </Link>
                    <Link to='/aboutus'>
                        <Button variant="ghost">About Us</Button>
                    </Link>
                    <Link to='login'>
                        <Button colorScheme="green">Log in</Button>
                    </Link>
                </HStack>
            </Box>
        </Flex>
        
    )
}
