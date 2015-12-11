/*BEGIN_LEGAL 
Intel Open Source License 

Copyright (c) 2002-2015 Intel Corporation. All rights reserved.
 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.  Redistributions
in binary form must reproduce the above copyright notice, this list of
conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.  Neither the name of
the Intel Corporation nor the names of its contributors may be used to
endorse or promote products derived from this software without
specific prior written permission.
 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE INTEL OR
ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
END_LEGAL */
/* ===================================================================== */
/*
  @ORIGINAL_AUTHOR: Robert Cohn
*/

/* ===================================================================== */
/*! @file
 *  This file contains an ISA-portable PIN tool for tracing memory accesses.
 */

#include "pin.H"
#include <iostream>
#include <fstream>
#include <iomanip>
/* ===================================================================== */
/* Global Variables */
/* ===================================================================== */

std::ofstream TraceFile;

/* ===================================================================== */
/* Commandline Switches */
/* ===================================================================== */

KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE, "pintool",
    "o", "pinatrace.out", "specify trace file name");
KNOB<BOOL> KnobValues(KNOB_MODE_WRITEONCE, "pintool",
    "values", "1", "Output memory values reads and written");

PIN_LOCK lock;

INT32 numThreads = 0;
const INT32 MaxNumThreads = 10000;

  // 64byte linesize : 64 - 8
/*struct THREAD_DATA
{
    UINT64 _count;
    UINT8 _pad[PADSIZE];
};

THREAD_DATA icount[MaxNumThreads];*/

/* ===================================================================== */
/* Print Help Message                                                    */
/* ===================================================================== */

static INT32 Usage()
{
    cerr <<
        "This tool produces a memory address trace.\n"
        "For each (dynamic) instruction reading or writing to memory the the ip and ea are recorded\n"
        "\n";

    cerr << KNOB_BASE::StringKnobSummary();

    cerr << endl;

    return -1;
}


static VOID EmitMem(VOID * ea, INT32 size)
{
    if (!KnobValues)
        return;
    
    switch(size)
    {
      case 0:
        TraceFile << setw(1);
        break;
        
      case 1:
        TraceFile << static_cast<UINT32>(*static_cast<UINT8*>(ea));
        break;
        
      case 2:
        TraceFile << *static_cast<UINT16*>(ea);
        break;
        
      case 4:
        TraceFile << *static_cast<UINT32*>(ea);
        break;
        
      case 8:
        TraceFile << *static_cast<UINT64*>(ea);
        break;
        
      default:
        TraceFile.unsetf(ios::showbase);
        TraceFile << setw(1) << "0x";
        for (INT32 i = 0; i < size; i++)
        {
            TraceFile << static_cast<UINT32>(static_cast<UINT8*>(ea)[i]);
        }
        TraceFile.setf(ios::showbase);
        break;
    }
}

static VOID  PIN_FAST_ANALYSIS_CALL RecordMem(VOID * ip, CHAR r, VOID * addr, INT32 size, BOOL isPrefetch, THREADID tid)
{
   PIN_GetLock(&lock,tid+1);
   TraceFile <<tid<<"  "<<setw(1)
             <<ip<<setw(2+4*sizeof(ADDRINT))
             <<dec <<setw(2+6*sizeof(ADDRINT));
    
    if (!isPrefetch)
        EmitMem(addr, size);
    TraceFile << endl;
   PIN_ReleaseLock(&lock);
}

static VOID * WriteAddr;
static INT32 WriteSize;

static VOID RecordWriteAddrSize(VOID * addr, INT32 size)
{
    WriteAddr = addr;
    WriteSize = size;
}

VOID ThreadStart(THREADID threadid, CONTEXT *ctxt, INT32 flags, VOID *v)
{
    
    PIN_GetLock(&lock, threadid+1);
    numThreads++;
    PIN_ReleaseLock(&lock);
    
    ASSERT(numThreads <= MaxNumThreads, "Maximum number of threads exceeded\n");
}



static VOID RecordMemWrite(VOID * ip)
{
   /* RecordMem(ip, 'W', WriteAddr, WriteSize, false);*/
}

VOID Instruction(INS ins, VOID *v)
{

    // instruments loads using a predicated call, i.e.
    // the call happens iff the load will be actually executed
        
    if (INS_IsMemoryRead(ins) && INS_IsStandardMemop(ins))
    {
        INS_InsertPredicatedCall(
            ins, IPOINT_BEFORE, (AFUNPTR)RecordMem,IARG_FAST_ANALYSIS_CALL,
            IARG_INST_PTR,
            IARG_UINT32, 'R',
            IARG_MEMORYREAD_EA,
            IARG_MEMORYREAD_SIZE,
            IARG_BOOL, INS_IsPrefetch(ins),IARG_THREAD_ID,
            IARG_END);
    }
}



/* ===================================================================== */

VOID Fini(INT32 code, VOID *v)
{
    TraceFile << "#eof" << endl;
    
    TraceFile.close();
}

/* ===================================================================== */
/* Main                                                                  */
/* ===================================================================== */

int main(int argc, char *argv[])
{
    PIN_InitLock(&lock);
    string trace_header = string("#\n"
                                 "# Memory Access Trace Generated By Pin\n"
                                 "#\n");
    
    if( PIN_Init(argc,argv) )
    {
        return Usage();
    }
    
    TraceFile.open(KnobOutputFile.Value().c_str());
    TraceFile.write(trace_header.c_str(),trace_header.size());
    TraceFile.setf(ios::showbase);
    INS_AddInstrumentFunction(Instruction, 0);
    
    PIN_AddThreadStartFunction(ThreadStart, 0);
   /* PIN_AddThreadFiniFunction(ThreadFini, 0);*/

    PIN_AddFiniFunction(Fini, 0);

    // Never returns

    PIN_StartProgram();
    
    RecordMemWrite(0);
    RecordWriteAddrSize(0, 0);
    
    return 0;
}

/* ===================================================================== */
/* eof */
/* ===================================================================== */
