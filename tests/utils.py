"""
Utilities for the sleeper-h2h-tools test suite
"""

import hashlib
import hmac
import pickle

from sleeper_h2h.standings import Metadata

def read_metadata_from_signed_pickle(path: str, key: bytes) -> Metadata:

    """
    Checks a pickle file for the specified HMAC signature, then reads the file
    if the comparison passes

    PARAMETERS
    ----------
    path : str
        path to the pickle file

    key : bytes
        bytes string of the expected HMAC key

    RETURNS
    -------
    data : Metadata
        Metadata object loaded from signed pickle file

    RAISES
    ------
    exception : ValueError
        ValueError is raised when the supplied `key` does not match the HMAC
        digest of the file specified in `path`
    """

    with open(path, "rb") as f:

        ref_hmac = hmac.new(key, digestmod=hashlib.blake2b)
        mac_from_stream = f.read(ref_hmac.digest_size)
        data_from_stream = f.read()
        ref_hmac.update(data_from_stream)
        computed_mac = ref_hmac.digest()

        if hmac.compare_digest(computed_mac, mac_from_stream):
            return pickle.loads(data_from_stream)

        raise ValueError(
            "HMAC comparison failed, this pickle file does not contain the" +\
            " correct digest"
        )
