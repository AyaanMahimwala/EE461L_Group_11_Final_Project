import React from 'react'
import { Box, Button, HStack, Heading, Flex, Spacer } from '@chakra-ui/react'

export default function HeaderMenu() {
    return (
        <Flex m="4">
            <Box>
                <Heading>EE461L Final Project!</Heading>
            </Box>
            <Spacer />
            <Box>
                <HStack>
                    <Button variant="ghost">Home</Button>
                    <Button variant="ghost">About Us</Button>
                    <Button colorScheme="green">Log in</Button>
                </HStack>
            </Box>
        </Flex>
        
    )
}
