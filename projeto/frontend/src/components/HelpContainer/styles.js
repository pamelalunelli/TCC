import styled from 'styled-components'

export const StyledHelpContainer = styled.section`
`

StyledHelpContainer.Title = styled.h1`
    margin: 1em 0; /* Adicionando espaço vertical proporcional */
    ${({theme}) => theme.typography.title.xl};
`
StyledHelpContainer.IntermediateTitle = styled.h2`
    margin: 1em 0; /* Adicionando espaço vertical proporcional */
    ${({theme}) => theme.typography.title.lg}; /* Estilo intermediário */
`
StyledHelpContainer.Paragraph = styled.p(({theme}) =>`
    margin-top: ${theme.spacing.lg};
    margin-bottom: 1em; /* Adicionando espaço vertical proporcional */
    ${theme.typography.body.base};
`)
