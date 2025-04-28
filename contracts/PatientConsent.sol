// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PatientConsent {
    struct Consent {
        address patient;
        string dataHash;  // IPFS or any other hash to uniquely represent data
        uint timestamp;
        bool consentGiven;
    }

    // Mapping to store consent information for each patient
    mapping(address => Consent) public patientConsents;

    // Event to emit when a patient's consent is updated
    event ConsentUpdated(address patient, string dataHash, bool consentGiven, uint timestamp);

    // Function to store the patient's consent information
    function storeConsent(string memory dataHash, bool consentGiven) public {
        patientConsents[msg.sender] = Consent({
            patient: msg.sender,
            dataHash: dataHash,
            timestamp: block.timestamp,
            consentGiven: consentGiven
        });

        // Emit an event when consent is updated
        emit ConsentUpdated(msg.sender, dataHash, consentGiven, block.timestamp);
    }

    // Function to query a patient's consent
    function queryConsent(address patient) public view returns (bool consentGiven, uint timestamp, string memory dataHash) {
        Consent memory consent = patientConsents[patient];
        return (consent.consentGiven, consent.timestamp, consent.dataHash);
    }
}
