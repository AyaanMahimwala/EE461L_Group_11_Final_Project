import React from 'react'
import Layout from './Layout'
import DataSetTable from './DataSetTable'
import {Flex} from '@chakra-ui/react'

export default function Home() {
    return (
        <Layout>
            <Flex m='6' w='75%'>
                <DataSetTable/>
            </Flex>
        </Layout>
    )
}
