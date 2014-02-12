#include <Python.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


#include "scrypt-jane/scrypt-jane.h"
//#include "scrypt.h"

// yacoin: increasing Nfactor gradually
const unsigned char minNfactor = 4;
const unsigned char maxNfactor = 30;
int nChainStartTime = 1388949883;


#define max(a,b)            (((a) > (b)) ? (a) : (b))
#define min(a,b)            (((a) < (b)) ? (a) : (b))


unsigned char GetNfactor(int nTimestamp) {
	int l = 0, s, n;
	unsigned char N;

	if (nTimestamp <= nChainStartTime)
		return 4;

	s = nTimestamp - nChainStartTime;
	while ((s >> 1) > 3) {
		l += 1;
		s >>= 1;
	}

	s &= 3;

	n = (l * 170 + s * 25 - 2320) / 100;

	if (n < 0) n = 0;

	if (n > 255)
		printf("GetNfactor(%d) - something wrong(n == %d)\n", nTimestamp, n);

	N = (unsigned char)n;
	//printf("GetNfactor: %d -> %d %d : %d / %d\n", nTimestamp - nChainStartTime, l, s, n, min(max(N, minNfactor), maxNfactor));

	return min(max(N, minNfactor), maxNfactor);
}

void scrypt_hash(const void* input, size_t inputlen, uint32_t *res, unsigned char Nfactor)
{
	return scrypt((const unsigned char*)input, inputlen,
		(const unsigned char*)input, inputlen,
		Nfactor, 0, 0, (unsigned char*)res, 32);
}

static PyObject *scrypt_getpowhash(PyObject *self, PyObject *args)
{
    char *output;
	int timestamp;
    PyObject *value;
    PyStringObject *input;
    if (!PyArg_ParseTuple(args, "Si", &input, &timestamp))
        return NULL;

    Py_INCREF(input);

    output = (char *)PyMem_Malloc(32);
	memset(output, 0, 32);

	scrypt_hash((char *)PyString_AsString((PyObject*) input), 80, (uint32_t *)output, GetNfactor(timestamp));
    Py_DECREF(input);
    value = Py_BuildValue("s#", output, 32);
    PyMem_Free(output);
    return value;
}



static PyMethodDef ScryptMethods[] = {
    { "getPoWHash", scrypt_getpowhash, METH_VARARGS, "Returns the proof of work hash using scrypt" },
    { NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC inityac_scrypt(void) {
    (void) Py_InitModule("yac_scrypt", ScryptMethods);
}
