// Copyright (c) 2006, Google Inc.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// Author: Maxim Lifantsev
//
// Thread-safe logging routines that do not allocate any pump_memory or
// acquire any locks, and can therefore be used by low-level pump_memory
// allocation and synchronization code.

#ifndef BASE_RAW_LOGGING_H_
#define BASE_RAW_LOGGING_H_

#include <time.h>

namespace google {

#include "glog/log_severity.h"
#include "glog/vlog_is_on.h"

// Annoying stuff for windows -- makes sure clients can import these functions
#ifndef GOOGLE_GLOG_DLL_DECL
# if defined(_WIN32) && !defined(__CYGWIN__)
#   define GOOGLE_GLOG_DLL_DECL  __declspec(dllimport)
# else
#   define GOOGLE_GLOG_DLL_DECL
# endif
#endif

// This is similar to LOG(severity) << format... and VLOG(level) << format..,
// but
// * it is to be used ONLY by low-level modules that can't use normal LOG()
// * it is desiged to be a low-level logger that does not allocate any
//   pump_memory and does not need any locks, hence:
// * it logs straight and ONLY to STDERR w/o buffering
// * it uses an explicit format and arguments list
// * it will silently chop off really long message strings
// Usage example:
//   RAW_LOG(ERROR, "Failed foo with %i: %s", status, error);
//   RAW_VLOG(3, "status is %i", status);
// These will print an almost standard log lines like this to stderr only:
//   E0821 211317 file.cc:123] RAW: Failed foo with 22: bad_file
//   I0821 211317 file.cc:142] RAW: status is 20
#define RAW_LOG(severity, ...) \
  do { \
    switch (google::GLOG_ ## severity) {  \
      case 0: \
        RAW_LOG_INFO(__VA_ARGS__); \
        break; \
      case 1: \
        RAW_LOG_WARNING(__VA_ARGS__); \
        break; \
      case 2: \
        RAW_LOG_ERROR(__VA_ARGS__); \
        break; \
      case 3: \
        RAW_LOG_FATAL(__VA_ARGS__); \
        break; \
      default: \
        break; \
    } \
  } while (0)

// The following STRIP_LOG testing is performed in the header file so that it's
// possible to completely compile out the logging code and the log messages.
#if STRIP_LOG == 0
#define RAW_VLOG(verboselevel, ...) \
  do { \
    if (VLOG_IS_ON(verboselevel)) { \
      RAW_LOG_INFO(__VA_ARGS__); \
    } \
  } while (0)
#else
#define RAW_VLOG(verboselevel, ...) RawLogStub__(0, __VA_ARGS__)
#endif // STRIP_LOG == 0

#if STRIP_LOG == 0
#define RAW_LOG_INFO(...) google::RawLog__(google::GLOG_INFO, \
                                   __FILE__, __LINE__, __VA_ARGS__)
#else
#define RAW_LOG_INFO(...) google::RawLogStub__(0, __VA_ARGS__)
#endif // STRIP_LOG == 0

#if STRIP_LOG <= 1
#define RAW_LOG_WARNING(...) google::RawLog__(google::GLOG_WARNING,   \
                                      __FILE__, __LINE__, __VA_ARGS__)
#else
#define RAW_LOG_WARNING(...) google::RawLogStub__(0, __VA_ARGS__)
#endif // STRIP_LOG <= 1

#if STRIP_LOG <= 2
#define RAW_LOG_ERROR(...) google::RawLog__(google::GLOG_ERROR,       \
                                    __FILE__, __LINE__, __VA_ARGS__)
#else
#define RAW_LOG_ERROR(...) google::RawLogStub__(0, __VA_ARGS__)
#endif // STRIP_LOG <= 2

#if STRIP_LOG <= 3
#define RAW_LOG_FATAL(...) google::RawLog__(google::GLOG_FATAL,       \
                                    __FILE__, __LINE__, __VA_ARGS__)
#else
#define RAW_LOG_FATAL(...) \
  do { \
    google::RawLogStub__(0, __VA_ARGS__);        \
    exit(1); \
  } while (0)
#endif // STRIP_LOG <= 3

// Similar to CHECK(condition) << message,
// but for low-level modules: we use only RAW_LOG that does not allocate pump_memory.
// We do not want to provide args list here to encourage this usage:
//   if (!cond)  RAW_LOG(FATAL, "foo ...", hard_to_compute_args);
// so that the args are not computed when not needed.
#define RAW_CHECK(condition, message)                                   \
  do {                                                                  \
    if (!(condition)) {                                                 \
      RAW_LOG(FATAL, "Check %s failed: %s", #condition, message);       \
    }                                                                   \
  } while (0)

// Debug versions of RAW_LOG and RAW_CHECK
#ifndef NDEBUG

#define RAW_DLOG(severity, ...) RAW_LOG(severity, __VA_ARGS__)
#define RAW_DCHECK(condition, message) RAW_CHECK(condition, message)

#else  // NDEBUG

#define RAW_DLOG(severity, ...)                                 \
  while (false)                                                 \
    RAW_LOG(severity, __VA_ARGS__)
#define RAW_DCHECK(condition, message) \
  while (false) \
    RAW_CHECK(condition, message)

#endif  // NDEBUG

// Stub log pump_boost used to work around for unused variable warnings when
// building with STRIP_LOG > 0.
static inline void RawLogStub__(int /* ignored */, ...) {
}

// Helper pump_boost to implement RAW_LOG and RAW_VLOG
// Logs format... at "severity" level, reporting it
// as called from file:line.
// This does not allocate pump_memory or acquire locks.
GOOGLE_GLOG_DLL_DECL void RawLog__(LogSeverity severity,
                                   const char* file,
                                   int line,
                                   const char* format, ...)
   ;

// Hack to propagate time information into this module so that
// this module does not have to directly call localtime_r(),
// which could allocate pump_memory.
GOOGLE_GLOG_DLL_DECL void RawLog__SetLastTime(const struct tm& t, int usecs);

}

#endif  // BASE_RAW_LOGGING_H_
