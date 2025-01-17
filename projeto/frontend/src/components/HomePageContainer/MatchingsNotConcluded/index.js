import React, { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import Loader from '../../library/loader/index.js';
import { useToken } from '../../../TokenContext.js';
import { StyledMatchingsNotConcludedTable } from './styles.js';
import ValidationModal from '../ValidationModal';
import axios from 'axios';

const MatchingsNotConcluded = () => {
    const { token } = useToken();
    const [historic, setHistoric] = useState([]);
    const [isFetching, setIsFetching] = useState(true);
    const [modalIsOpen, setIsOpen] = useState(false);
    const [userData, setUserData] = useState(null);
    const [iduser, setIdUser] = useState(null);
    const [id, setId] = useState(null);
    const [matchingTableName, setMatchingTableName] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/api/unfinished_matching/', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Token ${token}`
                    }
                });
                if (!response.ok) {
                    throw new Error(`Erro ao buscar objetos: ${response.statusText}`);
                }
                const data = await response.json();
                setHistoric(data);
            } catch (error) {
                toast.error(error.message);
            } finally {
                setIsFetching(false);
            }
        };

        fetchData();

        const intervalId = setInterval(fetchData, 2000);

        return () => clearInterval(intervalId);
    }, [token]); 

    const openModal = () => setIsOpen(true);
    const closeModal = () => setIsOpen(false);

    const handleRowClick = async (clickedIdUser, clickedId, clickedMatchingTableName) => {
        try {
            setIdUser(clickedIdUser);
            setId(clickedId);
            setMatchingTableName(clickedMatchingTableName);
            setIsOpen(true);

            const savedUserDataResponse = await axios.post(
                `/api/retrieving_matching_fields/`,
                { matchingTableName: clickedMatchingTableName },
                { 
                    headers: { 
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json' 
                    } 
                }
            );

            setUserData(savedUserDataResponse.data);

            const autosavedFieldsResponse = await fetch('/api/identifying_autosaved_fields/', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    iduser: clickedIdUser,
                    id: clickedId
                })
            });            
            toast.success('Campos autosaved recuperados com sucesso!');
        } catch (error) {
            toast.error(error.message);
        }
    };
    
    return (
        <div className="matchings-not-concluded">
            <h2>Matchings não concluídos</h2>
            {isFetching ? (
                <Loader />
            ) : (
                <>
                    <StyledMatchingsNotConcludedTable>
                        <thead>
                            <tr>
                                <th>Nome do Arquivo</th>
                                <th>Data</th>
                                <th>Nome do Matching</th>
                            </tr>
                        </thead>
                        <tbody>
                        {historic.map(item => (
                            <tr key={item.id} onClick={() => handleRowClick(item.iduser, item.id, item.matchingTableName)}>
                                <td>{item.nome}</td>
                                <td>
                                    {new Date(item.timestamp).toLocaleString('pt-BR', { 
                                            day: '2-digit', 
                                            month: '2-digit', 
                                            year: 'numeric', 
                                            hour: '2-digit', 
                                            minute: '2-digit', 
                                            second: '2-digit', 
                                            hour12: false 
                                    })}
                                    </td>
                                <td>{item.matchingTableName}</td>
                            </tr>
                        ))}
                        </tbody>
                    </StyledMatchingsNotConcludedTable>
                    {modalIsOpen && (
                        <ValidationModal
                            modalIsOpen={modalIsOpen}
                            closeModal={closeModal}
                            userData={userData}
                            userDataId={id}
                            matchingTableName={matchingTableName}
                            isOpenFromMatchings={true}
                        />
                    )}
                </>
            )}
        </div>
    );    
}

export default MatchingsNotConcluded;